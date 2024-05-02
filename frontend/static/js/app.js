let id_mensaje = 0;
let controller = null;

// --------------------------------------------------
//                    functions
// --------------------------------------------------

function format_chatbot_mesage(id){

  const chatbotMessage = `
  <div class='chatbot-message col-12 py-4 d-flex justify-content-center' id='${id}' style='display:none;'>
      <div class='d-flex col-8' id='chatbot-message-content'>
          <img src='static/imgs/chatbot.png' width='40' height='40'>
          <div class='m-2'>
              <h6>Edgebot</h6>
              <div class='container-animacion'>
                <div class='cargando'>
                  <div class='pelotas'></div>
                  <div class='pelotas'></div>
                  <div class='pelotas'></div>
                </div>
              </div>
          </div>
      </div>
  </div>`;

  return chatbotMessage;

}

function format_user_mesage(message){

  const userMessage = `
  <div class='user-message col-12 py-4 d-flex justify-content-center'>
      <div class='d-flex col-8' id='user-message-content'>
          <img src='static/imgs/user.png' width='40' height='40'>
          <div class='m-2'>
              <h6>Tú</h6>
              <p>${message}</p>
          </div>
      </div>
  </div>`;

  return userMessage;

}

function disable_form_message(){
  $('#btn-enviar').hide();
  $('#btn-detener').show();
  $('#input-message').prop('disabled', true);
}

function enable_form_message(){
  let send_button = $('#btn-enviar');
  send_button.css('background-color', '#565656');
  send_button.css('color', '#000000');
  send_button.prop('disabled', true);
  send_button.show();
  $('#btn-detener').hide();
  $('#input-message').prop('disabled', false);
}

function initialize(){
  let send_button = $('#btn-enviar');
  send_button.css('background-color', '#565656');
  send_button.css('color', '#000000');
  send_button.prop('disabled', true);
  $('#btn-detener').hide();
}

function get_message(){
  const message = $('#input-message').val();
  $('#input-message').val('');
  return message;
}

async function send_message(message, signal){
  const url = 'https://fastapi-chatbot-guitarstore.onrender.com/api/v1/chatbot/msg';
  //let url = '';
  const response = await fetch(url, {
    signal: signal,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({message:message})
  }).then(response => response.json())
    .then(data => data
    ).catch(error => {
      if (error.name === 'AbortError') {
        return {'msg':'<h7 class="text-danger">El mensaje fue cancelado<h7>'};
      } else {
        console.error('Error en la solicitud:', error);
      }
    });

  return response;
}

// --------------------------------------------------
//                      events
// --------------------------------------------------

$('#input-message').on('keyup', function(event){

  let text = $(this).val();
  let button = $('#btn-enviar');

  if(text.trim() === ""){
    button.css('color', '#000000');
    button.css('background-color', '#565656');
    button.prop('disabled', true);
  }else{
    if (event.keyCode === 13) {
      button.trigger('click');
    }

    button.css('color', '#ffffff');
    button.css('background-color', '#007bff');
    button.prop('disabled', false);
  }

});

$('#btn-enviar').on('click', async function(){

  disable_form_message();
  const userMessage = get_message();

  // getting identifier to add in chatbot message
  const id = 'container-chatbot-message-'+id_mensaje++;
  const formattedChatbotMessage = format_chatbot_mesage(id);
  const formattedUserMessage = format_user_mesage(userMessage);

  // adding messages to conversation
  $('.conversation').append(formattedUserMessage);
  $('.conversation').append(formattedChatbotMessage);

  window.scrollTo(0, document.documentElement.scrollHeight);

  // sending message to chatbot
  controller = new AbortController();
  const signal = controller.signal;
  const response = await send_message('Se te dará una pregunta que debes responder retornando en formato de markdown. pregunta de usuario: '+userMessage, signal);

  // adding bot message to conversation
  $('.container-animacion').remove();
  $(`#${id}`).fadeIn();
  const converter = new showdown.Converter();
  const htmlOutput = converter.makeHtml(response['msg']);

  let images = '';

  if(response['images']){
    response['images'].forEach(image => {
      images += `<img src='${image}' class='rounded float-left img-thumbnail' width='200' height='200'>`;
    });
  }

  $(`#${id} .m-2`).append(`<p>
    ${htmlOutput}
    ${images}
  </p>`);

  window.scrollTo(0, document.documentElement.scrollHeight);

  enable_form_message();

});

$('#btn-detener').on('click', function(){
  enable_form_message();
  if (controller) {
    controller.abort(); // Se llama al método abort() del controlador para cancelar la petición
    console.log('Petición cancelada');
  }
});

// --------------------------------------------------
//                 initialization
// --------------------------------------------------

$(document).ready(function() {
  initialize();

  $(".loader-wrapper").fadeOut(1200, function() {
    $("#contenido").fadeIn(1500);
  });
});


//$( document ).ready(function(){});
//$( window ).on( "load", function(){});
