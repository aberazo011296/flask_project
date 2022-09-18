var app = angular.module('music_events', []);
app.controller('UsuarioCtrl', function ($scope, $http) {

    $scope.api_server = "http://localhost:5000/";

    $scope.usuario = {
        identificacion: '',
        nombres: '',
        apellidos: '',
        email: '',
        password: '',
        descripcion: '',
        direccion: '',
        celular: '',
        fecha_nacimiento: '',
        nacionalidad: '',
        avatar: '',
        video: '',
        rol_id: '',
        genero_id: '',
        instrumentos_ids:[]
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

    $scope.update = function (id) {
        $http({
            method: 'POST',
            url: $scope.api_server + 'editar/usuario/'+id,
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

    $scope.actualizarChosen = function () {
        console.log("entro");
        $('.selectpicker').selectpicker('refresh')
    }

    setTimeout(function () {
        $('.selectpicker').selectpicker('refresh');
    }, 1000);

});