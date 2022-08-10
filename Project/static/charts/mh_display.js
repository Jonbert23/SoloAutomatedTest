(function defaultDisplay() 
{
    document.getElementById("mail").hidden = true;
    document.getElementById("scorecard").hidden = true;
})();

function testType() 
{
    const myElement = document.getElementById("selectToDisplay").value;
    if(myElement == 'Mail')
    {
        document.getElementById("mail").hidden = false;
        document.getElementById("module").hidden = true;
        document.getElementById("scorecard").hidden = true;
        console.log('Mail ',myElement);
    }
    if(myElement == 'Module') 
    {
        document.getElementById("mail").hidden = true;
        document.getElementById("module").hidden = false;
        document.getElementById("scorecard").hidden = true;
        console.log('Module', myElement);
    }
    if(myElement == 'Scorecard') 
    {
        document.getElementById("mail").hidden = true;
        document.getElementById("module").hidden = true;
        document.getElementById("scorecard").hidden = false;
        console.log('Module', myElement);
    }
}
document.getElementById("mail_creds").hidden = true;

function mail_creds_display()
{
    var mail = document.getElementById("mail_checkbox");

    if(mail.checked)
    {
        console.log('checked');
        document.getElementById("mail_creds").hidden = false;
        document.getElementById("email_username").required = true;
        document.getElementById("mail_password").required = true;
    }
    else
    {
        console.log('unchecked');
        document.getElementById("mail_creds").hidden = true;
        document.getElementById("email_username").required = false;
        document.getElementById("mail_password").required = false;
    }

}
