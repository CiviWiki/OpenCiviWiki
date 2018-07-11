// CSRF Setup

const csrfSafeMethod = method => /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
const CSRFToken = () => {
  const csrftoken = $('[name=csrfmiddlewaretoken]').val();

  $.ajaxSetup({
    beforeSend(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    },
  });
};
export default CSRFToken;
