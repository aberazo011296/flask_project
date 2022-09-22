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
        avatar_filename: '',
        video: '',
        video_filename: '',
        rol_id: '',
        genero_id: '',
        instrumentos_ids:[]
    };

    $scope.calificacion = 0;

    $scope.create = function () {
        console.log($scope.usuario.avatar);
        if($scope.usuarios_form.$valid){
            if($scope.usuario.avatar === "" || typeof($scope.usuario.avatar) == 'undefined'){
                toastr.error("Foto de avatar no subido");
            } else if($scope.usuario.video === "" || typeof($scope.usuario.video) == 'undefined'){
                toastr.error("Video no subido");
            } else {
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
                    toastr.error(response.data.message);
                });
            }
        } else {
            toastr.error("Formulario con datos incorrectos");
        }
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
            toastr.error(response.data.message);
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

    $scope.SelectFile = function (e) {
        const file = e.target.files[0];
        $scope.usuario.avatar_filename = e.target.files[0].name
        // Encode the file using the FileReader API
        const reader = new FileReader();
        reader.onloadend = () => {
            // Use a regex to remove data url part
            const base64String = reader.result
                .replace('data:', '')
                .replace(/^.+,/, '');

            console.log(base64String);
            $scope.usuario.avatar = base64String;
            // Logs wL2dvYWwgbW9yZ...
        };
        reader.readAsDataURL(file);

    };

    $scope.SelectFileVideo = function (e) {
        const file = e.target.files[0];
        $scope.usuario.video_filename = e.target.files[0].name
        // Encode the file using the FileReader API
        const reader = new FileReader();
        reader.onloadend = () => {
            // Use a regex to remove data url part
            const base64String = reader.result
                .replace('data:', '')
                .replace(/^.+,/, '');

            console.log(base64String);
            $scope.usuario.video = base64String;
            // Logs wL2dvYWwgbW9yZ...
        };
        reader.readAsDataURL(file);
    };

});