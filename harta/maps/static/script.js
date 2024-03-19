    var map;
    var marker;
    var civicMarker;

    function create2DMap() {
      map = L.map('map').setView([45.657975, 25.601198], 15);

      var standardLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
      map.addLayer(standardLayer);

      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
          var userLat = position.coords.latitude;
          var userLng = position.coords.longitude;

          L.marker([userLat, userLng], { icon: getOrangeIcon() }).addTo(map)
            .bindPopup("Locația ta curentă")
            .openPopup();

          document.getElementById("current-location").innerHTML = "Locatia ta curenta: Latitudine " + userLat.toFixed(4) + ", long " + userLng.toFixed(4);
        });
      }
      addMarker([45.64277777777778, 25.589166666666665], "Centru Vechi");
      addMarker([45.63583333333333, 25.580000000000002], "Schei");
      addMarker([45.666666666666664, 25.576666666666665], "Bartolomeu");
      addMarker([45.645833333333336, 25.580000000000002], "Locatie 4");
      addMarker([45.663333333333334, 25.618333333333336], "Locatie 5");
      addMarker([45.61333333333333, 25.63972222222222], "Locatie 6");
      addMarker([45.59583333333333, 25.554166666666667], "Locatie 7");
      addMarker([45.70805555555555, 25.575], "Locatie 8");
      addMarker([45.67638888888889, 25.644166666666663], "Locatie 9");
      addMarker([45.65722222222222, 25.59972222222222], "Locatie 10");
      addMarker([45.63416666666667, 25.607222222222223], "Locatie 11");
      addMarker([45.65222222222222, 25.620833333333334], "Locatie 12");

      civicMarker = addMarkerWithImages([45.65222222222222, 25.611666666666665], "Centru Civic");

      map.on('click', function (e) {
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;

        if (marker) {
          map.removeLayer(marker);
        }

        if (civicMarker) {
          civicMarker.closePopup();
          civicMarker = null;
          document.getElementById("image-container").style.display = "none";
        }

        var redIcon = L.icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });

        marker = L.marker([lat, lng], { icon: redIcon }).addTo(map)
          .bindPopup("Locația ta selectată")
          .openPopup();
      });

      function addMarker(coordinates, popupText) {
        L.marker(coordinates).addTo(map)
          .bindPopup(popupText)
          .openPopup();
      }

      function addMarkerWithImages(coordinates, popupText) {
        var marker = L.marker(coordinates).addTo(map);

        marker.bindPopup(popupText).on('popupopen', function () {
          // La deschiderea pop-up-ului, solicităm imaginile corespunzătoare centrului civic
          fetch('/get_images/')
            .then(response => response.json())
            .then(data => {
              displayImages(data.imagini);
            })
            .catch(error => console.error('Error:', error));
        });

        return marker;
      }

      function displayImages(images) {
        var imageContainer = document.getElementById("image-container");
        imageContainer.innerHTML = ""; // Curățăm conținutul anterior

        images.forEach(function (image) {
          var imgElement = document.createElement("img");
          imgElement.src = 'data:image/png;base64,' + image.imagine;
          imgElement.alt = image.nume;
          imageContainer.appendChild(imgElement);
        });

        // Afișăm containerul de imagini
        imageContainer.style.display = "block";
      }


      function getOrangeIcon() {
        return L.icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });
      }
    }

    create2DMap();
 