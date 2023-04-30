ymaps.ready(init);

    function init() {
        // Создание карты.
        if (document.getElementById("id_place").value) {
            center = [...document.getElementById("id_place").value.split(',')]
        }
        else {
            center = [92.852571, 56.010566]
        }
        //let center = [92.852571, 56.010566]
        var myMap = new ymaps.Map("map", {

            // Координаты центра карты.
            // Порядок по умолчнию: «широта, долгота» изменил на longlat.
            center: center,

            // Уровень масштабирования. Допустимые значения:
            // от 0 (весь мир) до 19.
            zoom: 12,
            // Элементы управления
            controls: [

                'zoomControl', // Ползунок масштаба
                'rulerControl', // Линейка
                // 'routeButtonControl', // Панель маршрутизации
                // 'trafficControl', // Пробки
                // 'typeSelector', // Переключатель слоев карты
                // 'fullscreenControl', // Полноэкранный режим

                // Поисковая строка
                new ymaps.control.SearchControl({
                    options: {
                        // вид - поисковая строка
                        size: 'medium',
                        // Включим возможность искать не только топонимы, но и организации.
                        provider: 'yandex#search'
                    }
                })

            ]
        });
        var myCollection = new ymaps.GeoObjectCollection();

        if (document.getElementById("id_place").value)
                {
                    try {
                        center = [...document.getElementById("id_place").value.split(',')]
                    } catch(e) {
                        center = [92.852571, 56.010566]
                    }

                    var myPlacemark = new ymaps.Placemark(center);
                    myCollection.add(myPlacemark)
                    myMap.geoObjects.add(myCollection);
                }




        myMap.events.add('click', function (e) {

            myCollection.removeAll();
            // Получение координат щелчка
            var coords = e.get('coords');
            var myPlacemark = new ymaps.Placemark([...coords]);
            myCollection.add(myPlacemark)
            myMap.geoObjects.add(myCollection);

            document.getElementById("id_place").value = coords.join(',');

        });

    }
