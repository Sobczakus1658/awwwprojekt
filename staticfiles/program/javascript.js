function rozwij_plik() {
  document.getElementById("plikDropdown").classList.toggle("show");
}
function standard() {
  document.getElementById("standard_dane").style.display = "block";
  document.getElementById("optymalizacje_dane").style.display = "none";
  document.getElementById("procesor_dane").style.display = "none";
  document.getElementById("zalezne_dane").style.display = "none";
}
function optymalizacje() {
  document.getElementById("standard_dane").style.display = "none";
  document.getElementById("optymalizacje_dane").style.display = "block";
  document.getElementById("procesor_dane").style.display = "none";
  document.getElementById("zalezne_dane").style.display = "none";
}
function procesor() {
  document.getElementById("standard_dane").style.display = "none";
  document.getElementById("optymalizacje_dane").style.display = "none";
  document.getElementById("procesor_dane").style.display = "block";
  document.getElementById("zalezne_dane").style.display = "none";
}
function zalezne() {
  document.getElementById("standard_dane").style.display = "none";
  document.getElementById("optymalizacje_dane").style.display = "none";
  document.getElementById("procesor_dane").style.display = "none";
  document.getElementById("zalezne_dane").style.display = "block";
}



var formularz1 = document.getElementById("mojFormularz_standard");
formularz1.addEventListener("submit", function (event) {
  event.preventDefault();

  var poleInformacji = document.querySelector('input[name="standard"]:checked');
  console.log(poleInformacji);
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/zmien_zmienna", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var odpowiedz = JSON.parse(xhr.responseText);
      console.log("Nowa wartość zmiennej: " + odpowiedz.nazwa);
    }
  };

  xhr.onerror = function () {
    console.log('Wystąpił błąd połączenia.');
  };

  var dane = {
    "nazwa": poleInformacji.name,
    "standard": poleInformacji.value
  };
  var jsonData = JSON.stringify(dane);

  xhr.send(jsonData);
});
var formularz2 = document.getElementById("mojFormularz_procesor");
formularz2.addEventListener("submit", function (event) {
  event.preventDefault();

  var poleInformacji = document.querySelector('input[name="procesor"]:checked');

  console.log(poleInformacji);
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/zmien_zmienna", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var odpowiedz = JSON.parse(xhr.responseText);
      console.log("Nowa wartość zmiennej: " + odpowiedz.nazwa);
    }
  };
  var myVariableElement = document.getElementById('myVariableElement');
  var variableElement = poleInformacji.value;
  if (variableElement == "mcs51") {
    document.getElementById("mcs51").style.display = "block";
    document.getElementById("z80").style.display = "none";
    document.getElementById("ds390").style.display = "none";
  }
  if (variableElement == "z80") {
    document.getElementById("mcs51").style.display = "none";
    document.getElementById("z80").style.display = "block";
    document.getElementById("ds390").style.display = "none";
  }
  if (variableElement == "ds390") {
    document.getElementById("mcs51").style.display = "none";
    document.getElementById("z80").style.display = "none";
    document.getElementById("ds390").style.display = "block";
  }
  xhr.onerror = function () {
    console.log('Wystąpił błąd połączenia.');
  };

  var dane = {
    "nazwa": poleInformacji.name,
    "procesor": poleInformacji.value
  };
  var jsonData = JSON.stringify(dane);

  xhr.send(jsonData);
});
var formularz3 = document.getElementById("mojFormularz_optymalizacje");
formularz3.addEventListener("submit", function (event) {
  event.preventDefault(); // Zapobieganie domyślnej akcji formularza

  var poleInformacji = document.querySelectorAll('input[name="optymalizacje"]:checked');
  var opcje = Array.from(poleInformacji).map(function (informacje) {
    return informacje.value;
  });
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/zmien_zmienna", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var odpowiedz = JSON.parse(xhr.responseText);
      console.log("Nowa wartość zmiennej: " + odpowiedz.nazwa);
    }
  };
  xhr.onerror = function () {
    console.log('Wystąpił błąd połączenia.');
  };
  var wybraneOptymalizacje = Array.from(poleInformacji).map(function (pole) {
    return pole.value;
  });
  var optymalizacje = wybraneOptymalizacje.join(", ");
  console.log(opcje);
  var dane = {
    "nazwa": 'optymalizacje',
    "optymalizacje": opcje,
  };
  var jsonData = JSON.stringify(dane);

  xhr.send(jsonData);
});
var formularz4 = document.getElementById("mojFormularz_zalezne");
formularz4.addEventListener("submit", function (event) {
  event.preventDefault();
  var poleInformacji = document.querySelector('input[name="zalezne"]:checked');
  console.log(poleInformacji);
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/zmien_zmienna", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var odpowiedz = JSON.parse(xhr.responseText);
      console.log("Nowa wartość zmiennej: " + odpowiedz.nazwa);
    }
  };

  xhr.onerror = function () {
    console.log('Wystąpił błąd połączenia.');
  };

  var dane = {
    "nazwa": poleInformacji.name,
    "zalezne": poleInformacji.value
  };
  var jsonData = JSON.stringify(dane);

  xhr.send(jsonData);

  $('#kompilacja').show();
});
$(document).ready(function () {
  $('#create-directory-form').click(function () {
    event.preventDefault();
    $('#tworzenie_katalogu').show();
  });
  $('#tworzenie_pliku').click(function () {
    event.preventDefault();
    $('#tworzenie_nowego_pliku').show();
  });
  $('#anuluj-button').click(function () {
    $('#tworzenie_katalogu').hide();
  });

  $('#kompilacja_form').click(function () {
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/kompiluj", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    var dane = {
      "nazwa": ""
    };
    var jsonData = JSON.stringify(dane);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var odpowiedz = JSON.parse(xhr.responseText);
        console.log("Standard output: " + odpowiedz.stdout);
        console.log("Standard error: " + odpowiedz.stderr);
        console.log("Status: " + odpowiedz.status);
        $("#fragment").html(odpowiedz.stderr);
      }
    };
    xhr.send(jsonData);
  });

  $('#stworz_katalog').submit(function (event) {
    event.preventDefault();
    var formData = $(this).serializeArray();
    var dane = {};
    $.each(formData, function (index, field) {
      dane[field.name] = field.value;
    });

    console.log(dane);
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/stworz_katalog", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    var dane_do_wyslania = {
      "nazwa": dane['nazwa'],
      "rodzic": dane['rodzic']
    };
    console.log(dane_do_wyslania);
    xhr.send(JSON.stringify(dane_do_wyslania));
    function wypiszKatalog(katalog) {
      var elementListy = $('<li>').text(katalog.nazwa);
      if (katalog.podkatalogi.length > 0) {
        var podkatalogiContainer = $('<ul>');
        for (var i = 0; i < katalog.podkatalogi.length; i++) {
          var podkatalog = katalog.podkatalogi[i];
          var elementPodkatalogu = wypiszKatalog(podkatalog);
          podkatalogiContainer.append(elementPodkatalogu);
        }
        elementListy.append(podkatalogiContainer);
      }
      if (katalog.podpliki.length > 0) {
        var podplikiContainer = $('<ul>');
        for (var j = 0; j < katalog.podpliki.length; j++) {
          var podplik = katalog.podpliki[j];
          var elementPodpliku = $('<li>').text(podplik.nazwa);
          podplikiContainer.append(elementPodpliku);
        }
        elementListy.append(podplikiContainer);
      }
      $('#tworzenie_katalogu').hide();
      return elementListy;
    }
    $.ajax({
      url: '/pobierz_katalogi',
      type: 'GET',
      dataType: 'json',

      success: function (response) {
        var listaKatalogow = $('<ul>');
        for (var i = 0; i < response.length; i++) {
          var katalog = response[i];
          var elementKatalogu = wypiszKatalog(katalog);
          listaKatalogow.append(elementKatalogu);
        }
        $('#katalogi-container').html(listaKatalogow);
      },
      error: function (xhr, status, error) {
        console.error('Wystąpił błąd podczas pobierania danych:', error);
      }
    });
  });
  $('#anuluj-plik').click(function (event) {
    event.preventDefault();
    $('#tworzenie_nowego_pliku').hide();

  });
  $('#stworz_plik').submit(function (event) {
    event.preventDefault();
    console.log("heeejo");

    // Uzyskaj wartość CSRF tokena
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    // Utwórz obiekt FormData i dodaj dane formularza
    var formData = new FormData(this);

    // Dodaj CSRF token do nagłówka żądania
    formData.append('csrfmiddlewaretoken', csrfToken);

    // Wysyłanie żądania AJAX do serwera
    $.ajax({
      url: '/stworz_plik',  // Zastąp 'twoj_adres_url' odpowiednim adresem URL
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        // Obsłuż odpowiedź serwera po udanym żądaniu
        console.log('Żądanie wysłane pomyślnie');
        console.log(response);
      },
      error: function (xhr, status, error) {
        // Obsłuż błąd żądania
        console.error('Wystąpił błąd podczas wysyłania żądania:', error);
      }
    });
  });
  //  $(document).ready(function() {
  //   $('#stworz_plik').submit(function(event) {
  //     event.preventDefault();
  //     // console.log("heeejo")

  //     // Uzyskaj wartość CSRF tokena
  //     var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  //     var xhr = new XMLHttpRequest();
  //     xhr.open("POST", "/stworz_plik", true);
  //     xhr.setRequestHeader("Content-Type", "application/json");
  //     xhr.setRequestHeader("X-CSRFToken", csrfToken);

  //     // Utwórz obiekt FormData i dodaj dane formularza
  //     var formData = new FormData(this);
  //     console.log(formData.get('nazwa'));
  //     // Dodaj CSRF token do nagłówka żądania
  //     // formData.append('csrfmiddlewaretoken', csrfToken);
  //     // console.log(formData);
  //     // event.preventDefault(); 
  //     // var poleInformacji = document.querySelector('input[name="zalezne"]:checked');
  //     // console.log(poleInformacji);
  //     // var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  //     // var xhr = new XMLHttpRequest();
  //     // xhr.open("POST", "/zmien_zmienna", true);
  //     // xhr.setRequestHeader("Content-Type", "application/json");
  //     // xhr.setRequestHeader("X-CSRFToken", csrfToken);
  //     xhr.onreadystatechange = function() {
  //       if (xhr.readyState === 4 && xhr.status === 200) {
  //      var odpowiedz = JSON.parse(xhr.responseText);
  //      console.log("Nowa wartość zmiennej: " + odpowiedz.nazwa);
  //    }
  //  };

  //     xhr.onerror = function() {
  //         console.log('Wystąpił błąd połączenia.');
  //     };

  //     var dane = {
  //         "nazwa" :formData.get('nazwa'),
  //         "rodzic": formData.get('rodzic')
  //     };
  //     var jsonData = JSON.stringify(dane);

  //     xhr.send(jsonData);
  // Wysyłanie żądania AJAX do serwera
  // $.ajax({
  //   url: '/stworz_plik',  // Zastąp 'twoj_adres_url' odpowiednim adresem URL
  //   type: 'POST',
  //   data: formData,
  //   processData: false,
  //   contentType: false,
  //   success: function(response) {
  //     // Obsłuż odpowiedź serwera po udanym żądaniu
  //     console.log('Żądanie wysłane pomyślnie');
  //     console.log(response);
  //   },
  //   error: function(xhr, status, error) {
  //     // Obsłuż błąd żądania
  //     console.error('Wystąpił błąd podczas wysyłania żądania:', error);
  //   }
  // });
  // });
  // });



});
function wypiszKatalog(katalog) {
  var elementListy = $('<li>').text(katalog.nazwa);
  if (katalog.podkatalogi.length > 0) {
    var podkatalogiContainer = $('<ul>');
    for (var i = 0; i < katalog.podkatalogi.length; i++) {
      var podkatalog = katalog.podkatalogi[i];
      var elementPodkatalogu = wypiszKatalog(podkatalog);
      podkatalogiContainer.append(elementPodkatalogu);
    }
    elementListy.append(podkatalogiContainer);
  }
  if (katalog.podpliki.length > 0) {
    var podplikiContainer = $('<ul>');
    for (var j = 0; j < katalog.podpliki.length; j++) {
      var podplik = katalog.podpliki[j];
      var elementPodpliku = $('<li>').text(podplik.nazwa);
      podplikiContainer.append(elementPodpliku);
    }
    elementListy.append(podplikiContainer);
  }
  return elementListy;
}

$.ajax({
  url: '/pobierz_katalogi',
  type: 'GET',
  dataType: 'json',

  success: function (response) {
    var listaKatalogow = $('<ul>');
    for (var i = 0; i < response.length; i++) {
      var katalog = response[i];
      var elementKatalogu = wypiszKatalog(katalog);
      listaKatalogow.append(elementKatalogu);
    }
    $('#katalogi-container').html(listaKatalogow);
  },
  error: function (xhr, status, error) {
    console.error('Wystąpił błąd podczas pobierania danych:', error);
  }
});
// $.ajax({
//   url: '/pobierz_katalogi',  
//   type: 'GET',
//   dataType: 'json',

//   success: function(response) {
//     var listaKatalogow = $('<ul>');
//     for (var i = 0; i < response.length; i++) {
//       var katalog = response[i];
//       var elementListy = $('<li>').text(katalog.nazwa);
//       listaKatalogow.append(elementListy);
//     }
//     $('#katalogi-container').html(listaKatalogow);
//   },
//   error: function(xhr, status, error) {
//     console.error('Wystąpił błąd podczas pobierania danych:', error);
//   }
// });