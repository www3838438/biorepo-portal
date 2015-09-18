function bindEmailFuncs() {
    var email = $('#id_email'),
        institution = $('#id_institution'),
        accountInputs = $('#account-information input'),
        accountLabels = $('#account-information label');


    var chopre = /\w+@email\.chop\.edu/,
        chop = "The Children's Hospital of Philadelphia";

    function check() {
        if (chopre.test(email.val())) {
            accountInputs.attr('disabled', true);
            accountLabels.css('color', '#999');
            institution.val(chop);
        } else {
            accountInputs.attr('disabled', false);
            accountLabels.css('color', '');
        }
    }
    
    check();
    email.keyup(check);
    email.blur(check);
}