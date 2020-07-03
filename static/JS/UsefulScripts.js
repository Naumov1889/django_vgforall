function readTextFile(filename)
{
    let file = "/static/" + filename;
    let text = "";
    let rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status === 0)
            {
                text = rawFile.responseText;
            }
        }
    };
    rawFile.send(null);
    return text;
}


function Paste_Home_Page_Content() {
    document.getElementById("Title").innerHTML = readTextFile("HomePageContent/Title.txt");
    document.getElementById("about_project").innerHTML = readTextFile("HomePageContent/About_project.txt");
    document.getElementById("aim").innerHTML = readTextFile("HomePageContent/Aim.txt");
    document.getElementById("contact_data").innerHTML = readTextFile("HomePageContent/Contact_data.txt");

}