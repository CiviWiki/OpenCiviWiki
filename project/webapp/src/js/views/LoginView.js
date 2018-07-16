import { View } from 'backbone.marionette';
import entryTemplate from 'Templates/components/Login/entry_base.html';
import loginTemplate from 'Templates/components/Login/login_base.html';
import registerTemplate from 'Templates/components/Login/register_base.html';

import 'Styles/login.less';

const LoginView = View.extend({
  template: entryTemplate,
  regions: {
    content: '#entry-content',
  },
  initialize() {
    this.register = false;
  },
  
  onRender() {
    if (this.register) {
      this.showChildView('content', new View({ template: registerTemplate }));
    } else {
      this.showChildView('content', new View({ template: loginTemplate }));
    }
  },

  events: {
    'click .login-button': 'login',
    'click .register-link': 'swapToRegister',
    'click .login-link': 'swapToLogin',
    'click .register-button': 'register',
    'keypress .login-input ': 'checkForEnter',
    'blur .login-input': 'usernameToLowerCase',
  },

  checkForEnter(event) {
    if (event.which === 13 && !e.shiftKey) {
      event.preventDefault();
      this.login();
    }
  },

  usernameToLowerCase() {
    const usernameInput = this.$('#username');
    const lower = usernameInput.val().toLowerCase();
    if (lower !== usernameInput.val()) {
      usernameInput.val(lower);
    }
  },

  login() {
    const username = this.$el.find('#username').val();
    const password = this.$el.find('#password').val();

    if (username && password) {
      $.ajax({
        type: 'POST',
        url: 'auth/login',
        data: {
          username,
          password,
        },
        success() {
          window.location.replace('/');
        },
        error(data) {
          if (data.status === 400 && data.responseJSON) {
            M.toast({ html: data.responseJSON.message });
          } else {
            M.toast({ html: data.statusText });
          }
        },
      });
    } else {
      M.toast({
        html: 'Please input your username and password',
      });
    }
  },

  swapToRegister() {
    this.register = true;
    this.renderForms();
  },

  swapToLogin() {
    this.register = false;
    this.renderForms();
  },

  register() {
    let email = this.$el.find('#email');

    const username = this.$el.find('#username').val();

    const password = this.$el.find('#password').val();

    if (!email.is(':valid')) {
      M.toast({ html: 'Please enter a valid email' });
    } else if (password && username) {
      email = email.val();

      $.ajax({
        type: 'POST',
        url: 'auth/register',
        data: {
          email,
          username,
          password,
        },
        success() {
          window.location.replace('/');
        },
        error(data) {
          if (data.status === 400) {
            _.each(data.responseJSON.errors, (error) => {
              M.toast({ html: error });
            });
          } else if (data.status === 500) {
            M.toast({ html: 'Internal Server Error' });
          } else {
            M.toast({ html: data.statusText });
          }
        },
      });
    } else {
      M.toast({ html: 'Please fill all the fields' });
    }
  },
});
export default LoginView;
