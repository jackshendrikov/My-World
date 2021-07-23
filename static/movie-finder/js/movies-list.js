document.querySelector(".grid").addEventListener("click", function () {
    document.querySelector(".list").classList.remove("active");
    document.querySelector(".grid").classList.add("active");
    document.querySelector(".movies-wrapper").classList.add("gridView");
    document.querySelector(".movies-wrapper").classList.remove("tableView");

    let arrayOfTitles = document.getElementsByClassName('movie-cell poster');
    let arrayOfRate = document.getElementsByClassName('movie-cell rating');

    let arrayOfGenres = document.getElementsByClassName('movie-cell genre');
    let arrayOfNetflix = document.getElementsByClassName('movie-cell netflix');
    let arrayOfIMDB = document.getElementsByClassName('movie-cell imdb-num');
    let arrayOfWatchlist = document.getElementsByClassName('movie-cell watchlist');
    let watchBtn = document.getElementsByClassName('watchlist-btn');

    let lengthOfArray=arrayOfGenres.length;

    for (let i=0; i<lengthOfArray; i++){
        arrayOfGenres[i].style.display='none';
        arrayOfNetflix[i].style.display='none';
        arrayOfIMDB[i].style.display='none';
        arrayOfWatchlist[i].style.display='none';

        arrayOfTitles[i].style.textAlign = "center";
        arrayOfRate[i].style.textAlign = "center";
        watchBtn[i].style.display='block';
    }
});

document.querySelector(".list").addEventListener("click", function () {
    document.querySelector(".grid").classList.remove("active");
    document.querySelector(".list").classList.add("active");
    document.querySelector(".movies-wrapper").classList.remove("gridView");
    document.querySelector(".movies-wrapper").classList.add("tableView");

    let arrayOfTitles = document.getElementsByClassName('movie-cell poster');
    let arrayOfRate = document.getElementsByClassName('movie-cell rating');

    let arrayOfGenres = document.getElementsByClassName('movie-cell genre');
    let arrayOfNetflix = document.getElementsByClassName('movie-cell netflix');
    let arrayOfIMDB = document.getElementsByClassName('movie-cell imdb-num');
    let arrayOfWatchlist = document.getElementsByClassName('movie-cell watchlist');
    let watchBtn = document.getElementsByClassName('watchlist-btn');

    let lengthOfArray=arrayOfGenres.length;

    for (let i=0; i<lengthOfArray; i++){
        arrayOfGenres[i].style.display='flex';
        arrayOfNetflix[i].style.display='flex';
        arrayOfIMDB[i].style.display='flex';
        arrayOfWatchlist[i].style.display='flex';

        arrayOfTitles[i].style.textAlign = "initial";
        arrayOfRate[i].style.textAlign = "initial";
        watchBtn[i].style.display='none';
    }
});