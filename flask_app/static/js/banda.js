
 var app = angular.module('music_events', []);
 app.controller('BandaCtrl', function ($scope, $http) {
 
     $scope.api_server = "http://localhost:5000/";

     $scope.banda = {
        nombre: '',
        num_integrantes: '',
        video_filename:'',
        avatar_filename: '',
        celular: '',
        email: '',
        opciones: '',
        genero_id: '',
     };
     
     $scope.calificacion = 0;
    
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
            url: $scope.api_server + 'calificar/banda/'+id,
            data: {
                calificacion: $scope.calificacion
            }
        }).then(function successCallback(response) {

            toastr.success(response.data.message);
            setTimeout(function () {
                window.location.href = $scope.api_server+'bandas';
            }, 2000);

        }, function errorCallback(response) {
            toastr.error("Ocurrió un error");
        });
    }
});