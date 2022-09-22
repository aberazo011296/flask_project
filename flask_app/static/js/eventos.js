var app = angular.module('music_events', []);
app.controller('EventoCtrl', function ($scope, $http) {

    $scope.api_server = "http://localhost:5000/";

    $scope.evento = {
        titulo: '',
        direccion: '',
        fecha: '',
        hora_inicio: '',
        hora_fin: '',
        opciones: '',
        num_integrantes:'',
        genero_id: '',
        instrumentos_ids:[]
    };

    $scope.create = function () {
        console.log($scope.evento)
        $http({
            method: 'POST',
            url: $scope.api_server + 'crear/evento',
            data: {
                eventos: $scope.evento
            }
        }).then(function successCallback(response) {
            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'eventos';
            }, 2000);
        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    };

    $scope.getEvento = function (evento_id) {
        $http({
            method: 'GET',
            url: $scope.api_server + 'eventos/obtener/' + evento_id
        }).then(function successCallback(response) {

            $scope.evento = response.data.evento;

        }, function errorCallback(response) {
            toastr.error("No se encontró URL");
        });
    };

    $scope.update = function (id) {
        $http({
            method: 'POST',
            url: $scope.api_server + 'editar/evento/'+id,
            data: {
                evento: $scope.evento
            }
        }).then(function successCallback(response) {

            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'eventos';
            }, 2000);

        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    };

    $scope.actualizarChosen = function () {
        console.log("entro");
        $('.selectpicker').selectpicker('refresh')
    }

    setTimeout(function () {
        $('.selectpicker').selectpicker('refresh');
    }, 1000);
    
    $scope.getEvento = function (evento_id) {
        $http({
            method: 'GET',
            url: $scope.api_server + 'eventos/obtener/' + evento_id
        }).then(function successCallback(response) {

            $scope.evento = response.data.evento;

        }, function errorCallback(response) {
            toastr.error("No se encontró URL");
        });
    };

    $scope.update = function (id) {
        $http({
            method: 'POST',
            url: $scope.api_server + 'editar/eventos/'+id,
            data: {
                evento: $scope.evento
            }
        }).then(function successCallback(response) {

            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'eventos';
            }, 2000);

        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    };

    $scope.calificar = function (posicion) {
        console.log(posicion)
        for (var i = 1; i < posicion + 1; i++){
            var estrella = document.getElementById("star"+i);
            estrella.classList.add("checked-stars");
        }

        for (var i = posicion+1; i < 6; i++){
            var estrella = document.getElementById("star"+i);
            estrella.classList.remove("checked-stars");
        }

        $scope.calificacion = posicion;
        
    };

    $scope.rating = function (id) {
        $http({
            method: 'POST',
            url: $scope.api_server + 'calificar/evento/'+id,
            data: {
                calificacion: $scope.calificacion
            }
        }).then(function successCallback(response) {

            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'eventos';
            }, 2000);

        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    }
});