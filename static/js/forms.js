var clickCounter;
window.addEventListener('load', (event) => {
    clickCounter = 1;
});
function addSeasons(){
    seasons = document.getElementById('seasons').value;
    list = document.getElementById('list_seasons');
    list.innerHTML = '';
    for(let i = 1; i <= seasons; ++i){
        name = 'season_' + String(i);
        list.innerHTML += '<label for="' + name + '">Sezon ' + String(i) + '</label><br>';
        list.innerHTML += 'Rok produkcji sezonu:'
        list.innerHTML += '<input type="number" name="' + name + '_prod" id="' + name + '_prod" min="1850" max="2030"><br>'
        list.innerHTML += 'Podaj liczbę odcinków:';
        list.innerHTML += '<input type="number" name="' + name + '" id="' + name + '" min="1" max="100" ' +  
        'onchange=addChapter(' + String(i) + ')><br>';
        list.innerHTML += '<div id="list_chapters' + String(i) + '" name="list_chapters' + String(i) + '"></div>'
    }
}
function addChapter(num){
    chapters = document.getElementById('season_' + String(num)).value;
    list = document.getElementById('list_chapters' + String(num));
    list.innerHTML = ''
    for(let i = 1; i <= chapters; ++i){
        name = 'chapter_' + String(num) + '_' + String(i);
        list.innerHTML += 'Nazwa odcinka: ' + String(i);
        list.innerHTML += '<input type="text" name="' + name + '" id="' + name + '" min="1" max="100" ><br>';
    }
}
function addNextMovieOrSeries(){
    list = document.getElementById('list');

    let label1 = document.createElement("label");
    label1.setAttribute("for", "ms_" + String(clickCounter));
    label1.innerHTML = 'Nazwa filmu lub serialu';
    list.appendChild(label1);
    list.appendChild(document.createElement("br"));
    let inputMovieOrSeries = document.createElement("input");
    inputMovieOrSeries.setAttribute("type", "text");
    inputMovieOrSeries.setAttribute("id", "ms_" + String(clickCounter));
    inputMovieOrSeries.setAttribute("name", "ms_" + String(clickCounter));
    list.appendChild(inputMovieOrSeries);
    list.appendChild(document.createElement("br"));

    let label2 = document.createElement("label");
    label2.setAttribute("for", "role_" + String(clickCounter));
    label2.innerHTML = 'Rola na planie';
    list.appendChild(label2);
    list.appendChild(document.createElement("br"));
    let inputRole = document.createElement("input");
    inputRole.setAttribute("type", "text");
    inputRole.setAttribute("id", "role_" + String(clickCounter));
    inputRole.setAttribute("name", "role_" + String(clickCounter));
    list.appendChild(inputRole);
    list.appendChild(document.createElement("br"));

    let label3 = document.createElement("label");
    label3.setAttribute("for", "character_" + String(clickCounter));
    label3.innerHTML = 'Postać';
    list.appendChild(label3);
    list.appendChild(document.createElement("br"));
    let inputCharacter = document.createElement("input");
    inputCharacter.setAttribute("type", "text");
    inputCharacter.setAttribute("id", "character_" + String(clickCounter));
    inputCharacter.setAttribute("name", "character_" + String(clickCounter));
    list.appendChild(inputCharacter);
    list.appendChild(document.createElement("br"));
    clickCounter++;
}
function removeLastMovieOrSeries(){
    list = document.getElementById('list');
    let childrenToRemove = 12;
    while(list.firstChild && childrenToRemove > 0){
        list.removeChild(list.lastChild);
        childrenToRemove--;
    }
    clickCounter--;
}