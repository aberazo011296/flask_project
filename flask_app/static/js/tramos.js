var app = angular.module('myApp', []);
app.controller('myCtrl', function ($scope, $http) {

    $scope.api_server = "http://54.205.156.15:80/";

    $scope.viaje = {
        tramos: [{
            origen: "",
            destino: "",
            medio_transporte_id: "",
            co2_x_km: "",
            km: 0.00,
            co2: 0.00
        }],
        viaje_id: "",
        km_totales: 0.00,
        co2_totales: 0.00
    };

    $scope.getCo2XKm = function (id_transporte) {

        $scope.co2_x_km = 0.00;

        fetch($scope.api_server + "medio-transporte/" + id_transporte, {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status == 'ok') {
                    $scope.co2_x_km = parseFloat(data.co2_x_km);
                } else {
                    toastr.error(data.message);
                }
            });

    };

    $scope.cacularCO2 = function (co2_x_km, km) {
        var co2 = 0.00;
        co2 = co2_x_km * parseFloat(km);
        $scope.calcularC02Total();
        return parseFloat(co2.toFixed(2));

    };

    $scope.dosDecimales = function (valor) {
        return parseFloat(parseFloat(valor).toFixed(2));
    };

    $scope.addTramo = function () {
        $scope.viaje.tramos.push({
            origen: "",
            destino: "",
            medio_transporte_id: "",
            co2_x_km: "",
            km: "",
            co2: ""
        });
    };

    $scope.removeTramo = function (id) {
        $scope.viaje.tramos.splice(id, 1);
        $scope.calcularC02Total();
    };

    $scope.calcularC02Total = function () {

        setTimeout(function () {

            $scope.viaje.co2_totales = 0.00;
            $scope.viaje.km_totales = 0.00;

            for (var i = 0; i < $scope.viaje.tramos.length; i++) {
                var tramo = $scope.viaje.tramos[i];
                $scope.viaje.co2_totales += parseFloat(tramo.co2);
                $scope.viaje.km_totales += parseFloat(tramo.km);
            }

            document.getElementsByName('total_co2')[0].value = $scope.viaje.co2_totales;
            document.getElementsByName('total_km')[0].value = $scope.viaje.km_totales;

        }, 500);

        $scope.show = true;
    };

    $scope.create = function () {

        if ($scope.tramos_form.$valid) {

            if ($scope.viaje.co2_totales === 0 && $scope.viaje.km_totales === 0) {
                toastr.error("No se ha realizado el cálculo");
            } else if($scope.viaje.tramos.length < 1){
                toastr.error("Ingrese tramos");
            } else {
                console.log($scope.viaje)
                $http({
                    method: 'POST',
                    url: $scope.api_server + 'tramos/create',
                    data: {
                        viaje: $scope.viaje
                    }
                }).then(function successCallback(response) {

                    toastr.success(response.data.message);
                    setTimeout(function () {
                        window.location.href = $scope.api_server+'dashboard';
                    }, 2000);

                }, function errorCallback(response) {
                    toastr.error("No se encontró URL");
                });
            }

        } else {
            toastr.error("Campos incompletos");
        }
    };

    $scope.armarTramos = function (viaje_id) {
        $http({
            method: 'GET',
            url: $scope.api_server + 'tramos/obtener/' + viaje_id
        }).then(function successCallback(response) {

            if(response.data.tramos.length > 0){
                $scope.viaje.tramos.splice(0, 1);
            }

            for (var i = 0; i < response.data.tramos.length; i++) {

                var tramo = response.data.tramos[i];

                var co2_x_km = $scope.getCo2XKm(tramo.medio_transporte_id.toString());
                
                tramo_js = {
                    origen: tramo.origen,
                    destino: tramo.destino,
                    medio_transporte_id: tramo.medio_transporte_id.toString(),
                    co2_x_km: co2_x_km,
                    km: tramo.km,
                    co2: tramo.co2
                }
                $scope.viaje.tramos.push(tramo_js);
            };

            console.log($scope.viaje);

        }, function errorCallback(response) {
            toastr.error("No se encontró URL");
        });
    };
});