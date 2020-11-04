function copyToClipboard(){
  console.log('event triggered');

}

$(document).ready(function(){

  var cp = new ClipboardJS('.btn-copy');

  $('.btn-copy').mouseleave(function(){
    $(this).tooltip('hide');
  });


  $("#id_editq-questionnaire_language").on('change', function(){
    var lang = $(this).val()


    if (lang == 'Pt')
    {
     $("#id_editq-title").val('Avaliação de {PRODUCT_NAME}');
     $("#id_editq-subtitle").val('Bem-vindo à avaliação de {PRODUCT_NAME}');
     $("#id_editq-paragraph").val('Com sua ajuda, gostaríamos de examinar como os usuários percebem a usabilidade e a estética do {PRODUCT_NAME}. Esperamos identificar áreas para otimização. Isso nos permitirá otimizar o produto de forma que seja o mais eficiente e compreensível possível.');
   } else if (lang =='Est') {
     $("#id_editq-title").val('Hinnang teenusele {PRODUCT_NAME}');
     $("#id_editq-subtitle").val('Tere tulemast toote {PRODUCT_NAME} hindamisse');
     $("#id_editq-paragraph").val('Teie abiga soovime uurida, kuidas kasutajad tajuvad toote {PRODUCT_NAME} kasutatavust ja esteetikat. Loodame kindlaks teha optimeerimise valdkonnad. See võimaldab meil toodet optimeerida nii, et see oleks võimalikult tõhus ja arusaadav.');
   } else {
     $("#id_editq-title").val('Assessment of {PRODUCT_NAME}');
     $("#id_editq-subtitle").val('Welcome to the assessment of {PRODUCT_NAME}');
     $("#id_editq-paragraph").val('Welcome to the assessment of {PRODUCT_NAME}! \n Thank you for taking time to participate in this stdy. My name is {OWNER_NAME}. Through this survey, I would like to undertsand how likely you are to trust {PRODUCT_NAME}. I would be very grateful if you complete this survey. This survey is anonymous. The record of your survey responses does not contain any identifying information about you. \n It will require approximately 10 minutes of your time. In case you have any questions, you can contact me via email {OWNER_EMAIL}');

   }





  });
});



$('#bologna-list a').on('click', function (e) {
  e.preventDefault()
  $(this).tab('show')
});
