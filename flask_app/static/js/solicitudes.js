var app = angular.module('music_events', []);
app.controller('SolicitudCtrl', function ($scope, $http) {

    $scope.api_server = "http://localhost:5000/";

    $scope.solicitud = {
        evento_id: '',
        usuario_id: '',
        estado: ''
    };

    $scope.create = function () {

        $http({
            method: 'POST',
            url: $scope.api_server + 'crear/usuario',
            data: {
                usuario: $scope.usuario
            }
        }).then(function successCallback(response) {
            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'usuarios';
            }, 2000);
        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    };

    $scope.getUsuario = function (usuario_id) {
        $http({
            method: 'GET',
            url: $scope.api_server + 'usuarios/obtener/' + usuario_id
        }).then(function successCallback(response) {

            $scope.usuario = response.data.usuario;

        }, function errorCallback(response) {
            toastr.error("No se encontró URL");
        });
    };

    $scope.update = function (evento_id, usuario_id, estado, num_integrantes) {
        $http({
            method: 'POST',
            url: $scope.api_server + 'editar/solicitud/'+evento_id+'/'+usuario_id,
            data: {
                estado: estado,
                num_integrantes: num_integrantes
            }
        }).then(function successCallback(response) {

            if(response.data.message === 'Evento llenó su cupo'){
                toastr.warning(response.data.message);
                setTimeout(function () {
                    window.location.href = $scope.api_server+'solicitudes';
                }, 2000);
            } else {
                toastr.success(response.data.message);
                setTimeout(function () {
                    window.location.href = $scope.api_server+'solicitudes';
                }, 2000);
            }

        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    };

    $scope.actualizarChosen = function () {
        $('.selectpicker').selectpicker('refresh')
    };

    setTimeout(function () {
        $('.selectpicker').selectpicker('refresh');
    }, 1000);

    $scope.calificar = function (posicion) {
        
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
            url: $scope.api_server + 'calificar/usuario/'+id,
            data: {
                calificacion: $scope.calificacion
            }
        }).then(function successCallback(response) {

            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'usuarios';
            }, 2000);

        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    }

});