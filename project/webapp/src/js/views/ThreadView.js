import { View } from 'backbone.marionette';

import { Civi } from '../models';

import EditThreadView;
import CiviView;
import NewResponseView;

const DEFAULTS = {
    types: ['problem', 'cause', 'solution'],
    types_plural: ['problems', 'causes', 'solutions'],
    civiViewStates: ['recommended', 'other'],
    viewLimit: 5,
};

const ThreadView = View.extend({
  el: '#thread',
  template: _.template($('#thread-template').html()),
  wikiTemplate: _.template($('#thread-wiki-template').html()),
  bodyTemplate: _.template($('#thread-body-template').html()),
  responseWrapper: _.template($('#thread-response-template').html()),
  outlineTemplate: _.template($('#outline-template').html()),

  initialize(options) {
    options = options || {};
    this.username = options.username;
    this.civis = options.civis;
    this.navExpanded = true;
    this.is_draft = options.is_draft;

    this.civiRecViewLimits = { problem: 0, cause: 0, solution: 0 };
    this.civiOtherViewLimits = { problem: 0, cause: 0, solution: 0 };
    this.civiRecViewTotals = { problem: 0, cause: 0, solution: 0 };
    this.civiOtherViewTotals = { problem: 0, cause: 0, solution: 0 };

    this.viewRecommended = true;
    this.recommendedCivis = [];
    this.otherCivis = [];
    this.outlineCivis = {};
    this.initRecommended();

    this.responseCollection = new cpw.ResponseCollection(
      {},
      {
        threadId: this.model.threadId,
      },
    );

    this.listenTo(this.responseCollection, 'sync', this.renderResponses);
    this.render();
  },

  initRecommended() {
    const view = this;
    this.recommendedCivis = [];
    this.otherCivis = [];
    this.civiRecViewTotals = { problem: 0, cause: 0, solution: 0 };
    this.civiOtherViewTotals = { problem: 0, cause: 0, solution: 0 };

    const civiRecViewLimits = { problem: 0, cause: 0, solution: 0 };


    const civiOtherViewLimits = { problem: 0, cause: 0, solution: 0 };
    // 1. Get id list of voted civis\
    const votes = this.model.get('user_votes');

    if (this.is_draft) {
      _.each(
        this.civis.models,
        (civi) => {
          this.recommendedCivis.push(civi.id);
        },
        this,
      );
    } else {
      _.each(
        this.civis.models,
        (civi) => {
          const voteData = _.findWhere(votes, { civi_id: civi.id });
          if (!_.isUndefined(voteData)) {
            civi.voted = true;
            const type = civi.get('type');
            if (type === 'problem') {
              civiRecViewLimits[type] += civiRecViewLimits[type];
              civiOtherViewLimits[type] += civiOtherViewLimits[type];
            } else if (
              voteData.activity_type === 'vote_pos'
              || voteData.activity_type === 'vote_vpos'
            ) {
              civiRecViewLimits[type] += civiRecViewLimits[type];
            } else {
              civiOtherViewLimits[type] += civiOtherViewLimits[type];
            }

            if (voteData.activity_type === 'vote_pos' || voteData.activity_type === 'vote_vpos') {
              _.each(
                civi.get('links'),
                (link) => {
                  const linkedCivi = this.civis.get(link);
                  if (linkedCivi) {
                    this.recommendedCivis.push(link);
                  }
                },
                this,
              );
            } else {
              _.each(
                civi.get('links'),
                (link) => {
                  const linkedCivi = this.civis.get(link);
                  if (linkedCivi) {
                    this.otherCivis.push(link);
                  }
                },
                this,
              );
            }
          } else {
            civi.voted = false;
          }
        },
        this,
      );
    }

    // Recommended civis pool takes precedence
    this.otherCivis = _.difference(this.otherCivis, this.recommendedCivis);

    _.each(
      this.civis.filterByType('problem'),
      (civi) => {
        this.recommendedCivis.push(civi.id);
        this.otherCivis.push(civi.id);
      },
      this,
    );

    _.each(
      DEFAULTS.types,
        (type) => {
        if (this.civiRecViewLimits[type] === 0) {
          if (civiRecViewLimits[type] < 5) {
            civiRecViewLimits[type] = 5;
          }
          this.civiRecViewLimits[type] = civiRecViewLimits[type];
        }
        if (this.civiOtherViewLimits[type] === 0) {
          if (civiOtherViewLimits[type] < 5) {
            civiOtherViewLimits[type] = 5;
          }
          this.civiOtherViewLimits[type] = civiOtherViewLimits[type];
        }
      },
      this,
    );
  },

  render() {
    this.$el.empty().append(this.template());

    this.editThreadView = new EditThreadView({
      model: this.model,
      parentView: this,
      threadId: this.model.threadId,
    });

    this.$('.thread-wiki-holder').addClass('hide');

    this.threadWikiRender();
    this.threadBodyRender();

    this.newCiviView = new NewCiviView({
      model: this.model,
      parentView: this,
    });

    this.renderBodyContents();
    this.scrollToBody();
  },

  threadWikiRender() {
    if (this.$('.thread-wiki-holder').length) {
      this.$('.thread-wiki-holder')
        .empty()
        .append(this.wikiTemplate());
    }
  },

  threadBodyRender() {
    const view = this;

    if (this.$('.thread-body-holder').length) {
      const bodyRenderData = {
        is_draft: this.is_draft,
      };
      this.$('.thread-body-holder')
        .empty()
        .append(this.bodyTemplate(bodyRenderData));

      this.$('.main-thread').on('scroll', (e) => {
        view.processCiviScroll();
      });
    }
  },

  renderBodyContents() {
    this.renderCivis();
    this.renderOutline();

    if (!this.is_draft) {
      this.renderVotes();
    }
  },

  renderOutline() {
    const view = this;
    if (this.civis.length === 0) {
      this.$('#civi-outline')
        .empty()
        .append(this.outlineTemplate());
    }

    // Render Outline Template based on models
    const problems = this.outlineCivis.problem;
    causes = this.outlineCivis.cause;
    solutions = this.outlineCivis.solution;

    const renderData = {
      problems,
      causes,
      solutions,
    };

    const recCount = { problem: 0, cause: 0, solution: 0 };
    const otherCount = { problem: 0, cause: 0, solution: 0 };
    const votes = this.model.get('user_votes');


    const voteIds = _.pluck(votes, 'civi_id');

    const counterCount = 0;
    _.each(view.civis.models, (c) => {
      const type = c.get('type');
      if (_.indexOf(voteIds, c.id) > -1) {
        // If part of current view setting
        if (_.indexOf(view.recommendedCivis, c.id) > -1) {
          recCount[type]++;
        } else if (_.indexOf(view.otherCivis, c.id) > -1) {
          otherCount[type]++;
        }
      }
    });

    const highlightCount = { problem: 0, cause: 0, solution: 0 };
    _.each(DEFAULTS.types, (type) => {
      if (view.viewRecommended) {
        highlightCount[type] = view.civiRecViewTotals[type];
      } else {
        highlightCount[type] = view.civiOtherViewTotals[type];
      }
    });
    let voteCount; let totalRec; let
      totalOther;
    if (this.viewRecommended) {
      voteCount = recCount;
    } else {
      voteCount = otherCount;
    }

    let count;
    if (this.is_draft) {
      count = {
        problem: highlightCount.problem,
        cause: highlightCount.cause,
        solution: highlightCount.solution,
      };
    } else {
      count = {
        problem: highlightCount.problem - recCount.problem,
        cause: highlightCount.cause - voteCount.cause,
        solution: highlightCount.solution - voteCount.solution,
      };
    }

    count.totalRec = this.civiRecViewTotals.problem
      + this.civiRecViewTotals.cause
      + this.civiRecViewTotals.solution
      - recCount.problem
      - recCount.cause
      - recCount.solution;
    count.totalOther = this.civiOtherViewTotals.problem
      + this.civiOtherViewTotals.cause
      + this.civiOtherViewTotals.solution
      - recCount.problem
      - otherCount.cause
      - otherCount.solution;

    renderData.count = count;
    renderData.is_draft = this.is_draft;

    this.$('#civi-outline')
      .empty()
      .append(this.outlineTemplate(renderData));
    this.$('#recommended-switch').attr('checked', this.viewRecommended);

    if (this.viewRecommended) {
      this.$('.label-recommended').addClass('current');
      this.$('.label-other').removeClass('current');
      this.$('.badge-recommended').addClass('current');
      this.$('.badge-other').removeClass('current');
      this.$('.civi-nav-count').removeClass('other');
    } else {
      this.$('.label-recommended').removeClass('current');
      this.$('.label-other').addClass('current');
      this.$('.badge-recommended').removeClass('current');
      this.$('.badge-other').addClass('current');
      this.$('.civi-nav-count').addClass('other');
    }
    // view more

    _.each(
      DEFAULTS.types,
      function (type) {
        const loadMore = this.$(`#thread-${type}s>.${type}-loader`);
        if (loadMore) {
          loadMore.clone().appendTo(`#${type}-nav`);
        }
      },
      this,
    );

    // Calculate tracking
    this.calcCiviLocations();
    // Padding so you can scroll and track the last civi element;
    const scrollPadding = this.$('.main-thread').height() - this.civiLocations[this.civiLocations.length - 1].height;
    this.$('.civi-padding').height(scrollPadding - 8);

    // Vote indication
    const outline = this.$('#civi-outline');
    _.each(
      this.model.get('user_votes'),
      (v) => {
        // var navItem = outline.find('#civi-nav-'+ v.civi_id);
        // navItem.before('<i class="material-icons tiny voted">beenhere</i>').addClass('nav-inactive');
        outline.find(`#civi-nav-${v.civi_id}`).addClass('nav-inactive');
        const navItemState = outline.find(`#civi-nav-state-${v.civi_id}`);
        navItemState.addClass('voted').text('beenhere');
      },
      this,
    );

    this.expandNav();
  },

  renderCivis() {
    this.$('#thread-problems').empty();
    this.$('#thread-causes').empty();
    this.$('#thread-solutions').empty();

    this.threadCivis = {};
    _.each(
      ['problem', 'cause', 'solution'],
      function (type) {
        let civis = this.civis.filterByType(type);
        // Filter by Recommended state if not 'problem' type
        const recCivis = _.filter(
          civis,
          function (c) {
            return _.indexOf(this.recommendedCivis, c.id) != -1;
          },
          this,
        );
        this.civiRecViewTotals[type] = recCivis.length;
        const otherCivis = _.filter(
          civis,
          function (c) {
            return _.indexOf(this.otherCivis, c.id) != -1;
          },
          this,
        );
        this.civiOtherViewTotals[type] = otherCivis.length;
        if (type != 'problem') {
          if (this.viewRecommended) {
            civis = recCivis;
          } else {
            civis = otherCivis;
          }
        }
        // Sort civi list by score
        civis = _.sortBy(civis, (civi) => {
          if (civi.voted) {
            return -civi.get('score') - 100;
          }
          return -civi.get('score');
        });

        // Cut by type view limit TODO: move to rendering

        let limit;
        if (this.viewRecommended) {
          limit = this.civiRecViewLimits[type];
        } else {
          limit = this.civiOtherViewLimits[type];
        }
        const totalCount = civis.length;

        if (totalCount > limit && !this.is_draft) {
          civis = civis.slice(0, limit);
          _.each(civis, this.civiRenderHelper, this);
          this.$(`#thread-${type}s`).append(
            `<div class="${
              type
            }-loader civi-load-more"><span class="civi-show-count">${
              limit
            }/${
              totalCount
            } ${
              type
            }s</span> <span class="btn-loadmore" data-civi-type="${
              type
            }">View More +</span></div>`,
          );
        } else {
          _.each(civis, this.civiRenderHelper, this);
        }

        this.outlineCivis[type] = civis;
      },
      this,
    );
  },

  civiRenderHelper(civi) {
    const is_draft = this.is_draft;
    const can_edit = civi.get('author').username == this.username;
    this.$(`#thread-${civi.get('type')}s`).append(
      new CiviView({
        model: civi, can_edit, is_draft, parentView: this,
      }).el,
    );
  },

  renderVotes() {
    const view = this;
    const savedVotes = this.model.get('user_votes');
    _.each(savedVotes, function (v) {
      this.$(`#civi-${v.civi_id}`)
        .find(`.${v.activity_type}`)
        .addClass('current');
    });
  },

  renderResponses() {
    this.$('.responses-box')
      .empty()
      .append(this.responseWrapper());
    this.newResponseView = new NewResponseView({
      model: this.model,
      parentView: this,
    });

    _.each(
      this.responseCollection.models,
      function (civi) {
        const can_edit = civi.get('author').username == this.username;
        const can_respond = this.civis.get(this.responseCollection.civiId).get('author').username == this.username;

        const new_civi_view = new CiviView({
          model: civi,
          can_edit,
          can_respond,
          parentView: this,
          response: true,
        });
        this.$('#response-list').append(new_civi_view.el);

        let vote = _.find(this.model.get('user_votes'), v => v.civi_id === civi.id);
        if (vote) {
          this.$(`#civi-${vote.civi_id}`)
            .find(`.${vote.activity_type}`)
            .addClass('current');
        }
        if (civi.get('rebuttal')) {
          const rebuttal_model = new cw.CiviModel(civi.get('rebuttal'));
          const rebuttal_can_edit = rebuttal_model.get('author').username == this.username;
          const rebuttal_view = new cw.CiviView({
            model: rebuttal_model,
            can_edit: rebuttal_can_edit,
            can_respond: false,
            parentView: this,
            response: true,
          });
          rebuttal_view.$('.civi-card').addClass('push-right');
          new_civi_view.el.after(rebuttal_view.el);

          vote = _.find(this.model.get('user_votes'), v => v.civi_id === rebuttal_model.id);
          if (vote) {
            this.$(`#civi-${vote.civi_id}`)
              .find(`.${vote.activity_type}`)
              .addClass('current');
          }
        }
      },
      this,
    );

    // add padding
    const $lastResponseCivi = this.$('#response-list div:last-child');
    const scrollPadding = this.$('.responses').height() - $lastResponseCivi.height();
    this.$('.responses-padding').height(scrollPadding - 8);
  },

  events: {
    'click .enter-body': 'scrollToBody',
    'click .enter-wiki': 'scrollToWiki',
    'click .expand-nav': 'toggleExpandNav',
    'click .civi-nav-link': 'goToCivi',
    'click .civi-card': 'drilldownCivi',
    'click .add-civi': 'openNewCiviModal',
    'click .add-response': 'openNewResponseModal',
    'click #recommended-switch': 'toggleRecommended',
    'click .btn-loadmore': 'loadMoreCivis',
    'click .edit-thread-button': 'openEditThreadModal',
    'click #js-publish-btn': 'publishThread',
  },

  scrollToBody() {
    const view = this;

    this.$('.thread-wiki-holder').addClass('hide');
    this.$('.thread-body-holder').removeClass('hide');
    this.$('.thread-body-holder').css({ display: 'block' });

    this.resizeBodyToWindow();

    this.renderOutline();
    this.processCiviScroll();
  },

  resizeBodyToWindow() {
    $('body').css({ overflow: 'hidden' });

    const $windowHeight = $('body').height();
    const bodyHeight = $windowHeight - $('#js-global-nav').height();

    const $civiNavScroll = this.$('.civi-outline');
    $civiNavScroll.css({ height: $windowHeight - $civiNavScroll.offset().top });
    const $civiThreadScroll = this.$('.main-thread');
    $civiThreadScroll.css({ height: $windowHeight - $civiThreadScroll.offset().top });
    const $civiResponseScroll = this.$('.responses');
    $civiResponseScroll.css({ height: $windowHeight - $civiResponseScroll.offset().top });
  },

  scrollToWiki() {
    const view = this;

    this.$('.thread-body-holder').addClass('hide');
    this.$('.thread-wiki-holder').removeClass('hide');
    $('body').css({ overflow: 'scroll' });
  },

  toggleExpandNav(e) {
    this.navExpanded = !this.navExpanded;
    this.expandNav(e);
  },

  expandNav(e) {
    const view = this;


    const $this = _.isUndefined(e) ? this.$('.expand-nav') : $(e.target);

    if (!this.navExpanded) {
      $('.civi-nav-wrapper').hide();
      $this.removeClass('expanded');
    } else {
      $('.civi-nav-wrapper').show();
      $this.addClass('expanded');
    }
    this.activateNav();
  },

  goToCivi(e) {
    const $link = $(e.target).closest('.civi-nav-link');
    this.$('.main-thread').animate(
      {
        scrollTop: _.findWhere(this.civiLocations, { id: $link.attr('data-civi-nav-id') }).top - 15,
      },
      250,
    );
  },

  calcCiviLocations() {
    const view = this;
    const threadPos = this.$('.main-thread').position().top;
    const scrollPos = this.$('.main-thread').scrollTop();
    this.civiLocations = [];
    // this.civiTops = [];
    // this.civiTargets =
    this.$('.civi-card').each((idx, civi) => {
      const $civi = $(civi);


      const $civiTop = $civi.position().top + scrollPos - threadPos;
      view.civiLocations.push({
        top: $civiTop,
        bottom: $civiTop + $civi.height(),
        height: $civi.height(),
        target: $civi,
        id: $civi.attr('data-civi-id'),
      });
    });
  },

  processCiviScroll() {
    const view = this;
    const scrollPosition = this.$('.main-thread').scrollTop();
    // 1. Check if there are any civis. No tracking if none
    if (this.civis.length === 0) {
      return;
    }

    // 2. Go through list of heights to get current active civi
    const OFFSET = 100;
    const element = _.find(
      this.civiLocations,
      function (l) {
        return (
          this.currentNavCivi !== l.id
          && scrollPosition >= l.top - OFFSET
          && scrollPosition < l.bottom - OFFSET
        );
      },
      this,
    );
    // 3. Activate Corresponding Civi Card and Nav
    if (!element) return;

    this.activateNav(element.id);
    this.autoscrollCivi(this.$(`#civi-${element.id}`));
  },

  activateNav(id) {
    const view = this;
    this.currentNavCivi = id || this.currentNavCivi;
    const $currentNavCivi = view.$(`[data-civi-nav-id="${view.currentNavCivi}"]`);

    if (!view.navExpanded) {
      this.$('.civi-nav-header').removeClass('current');
      $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
    } else {
      this.$('.civi-nav-link').removeClass('current');
      this.$('.civi-nav-header').removeClass('current');
      $currentNavCivi.addClass('current');
    }
  },

  autoscrollCivi(target) {
    const $this = target;

    const $currentCivi = this.$(`[data-civi-id="${this.currentCivi}"]`);


    const $newCivi = $this.closest('.civi-card');

    if (this.currentCivi !== $newCivi.attr('data-civi-id')) {
      // $currentCivi.removeClass('current');
      this.$('.civi-card').removeClass('current');
      $newCivi.addClass('current');
      const civi_id = $newCivi.data('civi-id');

      this.currentCivi = $newCivi.attr('data-civi-id');
      if (!_.isUndefined(this.currentCivi)) {
        this.responseCollection.civiId = this.currentCivi;
        this.responseCollection.fetch();
      }
    } else {
      $currentCivi.removeClass('current');
      this.$('.civi-card').removeClass('linked');

      this.currentCivi = null;
      this.$('.responses-box').empty();
    }
  },

  drilldownCivi(e) {
    const target = $(e.target);
    const ms_check = target.hasClass('ms-ctn')
      || target.hasClass('ms-sel-ctn')
      || target.hasClass('ms-close-btn')
      || target.hasClass('ms-trigger')
      || target.hasClass('ms-trigger-ico')
      || target.hasClass('ms-res-ctn')
      || target.hasClass('ms-sel-item')
      || target.hasClass('ms-res-group');

    if (
      target.hasClass('btn')
      || target.hasClass('rating-button')
      || target.is('input')
      || target.is('textarea')
      || target.is('label')
      || target.hasClass('input')
      || ms_check
    ) {
      return;
    }
    const $this = $(e.currentTarget);
    if (
      $this.find('.civi-type').text() != 'response'
      && $this.find('.civi-type').text() != 'rebuttal'
    ) {
      const $currentCivi = this.$(`[data-civi-id="${this.currentCivi}"]`);


      const $newCivi = $this.closest('.civi-card');

      if (this.currentCivi !== $newCivi.attr('data-civi-id')) {
        // $currentCivi.removeClass('current');
        this.$('.civi-card').removeClass('current');
        $newCivi.addClass('current');
        const civi_id = $newCivi.data('civi-id');

        this.currentCivi = $newCivi.attr('data-civi-id');

        this.responseCollection.civiId = this.currentCivi;
        this.responseCollection.fetch();
      } else {
        $currentCivi.removeClass('current');
        this.$('.civi-card').removeClass('linked');

        this.currentCivi = null;
        this.$('.responses-box').empty();
      }
    }
  },

  selectInitialCiviAfterToggle() {
    const $newCivi = this.$('.civi-card').first();

    $newCivi.addClass('current');
    this.currentCivi = $newCivi.attr('data-civi-id');

    this.responseCollection.civiId = this.currentCivi;
    this.responseCollection.fetch();
  },

  loadMoreCivis(e) {
    const $target = $(e.currentTarget);
    const type = $target.data('civi-type');
    let limit; let
      remaining;
    if (this.viewRecommended) {
      limit = this.civiRecViewLimits[type];
      remaining = this.civiRecViewTotals[type] - limit;
    } else {
      limit = this.civiOtherViewLimits[type];
      remaining = this.civiOtherViewTotals[type] - limit;
    }
    if (remaining <= 0) {
      return;
    }
    const addCount = cw.DEFAULTS.viewLimit < remaining ? cw.DEFAULTS.viewLimit : remaining;

    if (this.viewRecommended) {
      this.civiRecViewLimits[type] += addCount;
    } else {
      this.civiOtherViewLimits[type] += addCount;
    }
    this.renderBodyContents();
  },

  toggleRecommended(e) {
    const target = $(e.currentTarget);
    const recommendState = target.is(':checked');

    this.viewRecommended = recommendState;

    this.$('.main-thread').scrollTop(0);
    this.renderBodyContents();
    this.processCiviScroll();
    this.selectInitialCiviAfterToggle();
  },

  publishThread(e) {
    const view = this;
    view
      .$(e.currentTarget)
      .addClass('disabled')
      .attr('disabled', true);

    $.ajax({
      url: '/api/edit_thread/',
      type: 'POST',
      data: {
        thread_id: view.model.threadId,
        is_draft: false,
      },
      success() {
        view.is_draft = false;
        M.toast('Thread is now public. Refreshing the page...');
        view.$('#js-publish-btn').hide();
        _.delay(window.location.reload, 1000);
      },
      error(response) {
        if (response.status === 403) {
          M.toast('You do not have permission to publish the thread');
        } else if (response.status === 500) {
          M.toast('Server Error: Thread could not be published');
          view
            .$(e.currentTarget)
            .removeClass('disabled')
            .attr('disabled', false);
        }
      },
    });
  },

  openNewCiviModal() {
    this.newCiviView.render();
  },

  openNewResponseModal() {
    this.newResponseView.render();
  },

  openEditThreadModal() {
    this.editThreadView.render();
  },
});
export default ThreadView;
