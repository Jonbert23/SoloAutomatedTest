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
