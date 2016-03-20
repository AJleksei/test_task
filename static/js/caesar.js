angular.module("myApp", ['ngMessages'])
.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})
.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
})
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
})
.controller('CaesarController', function ($scope, $http){
    $scope.text = null;
    //$scope.letters_count = null;
    $scope.guess_rot = null;
    $scope.user_rot = null;
    $scope.is_guess = false;

    var loadSuccess = function (response) {
        $scope.text = response.data.text;
        //$scope.guess_rot = response.data.guess_rot;

        letters = [];
        $.each(response.data.letters_count, function(key, val){
            letters.push(val);
        });
        chart_data = {
            labels: Object.keys(response.data.letters_count),
            datasets: [
                {
                    label: "Letters rating",
                    fillColor: "rgba(0,102,204, 0.5)",// Цвет колонки
                    strokeColor: "rgba(0,51,153, 0.8)",// Цвет рамки, вокруг колонки
                    highlightFill: "rgba(0,51,153, 0.75)",
                    highlightStroke: "rgba(0,51,153, 1)",
                    data: letters
                }
            ]
        };

        createChart(chart_data);
    };

    var loadError = function (response) {
        /*
        $.each(response.data.errors, function(key, value){
            alert(value);
        });
        */
    };

    $scope.load = function ($event){
        original_text = $('#original_text').val();
        $scope.user_rot = $('#rot').val();
        action = $event.currentTarget.name;
        $scope.guess_rot = null;

        $http({
            url: 'coding_view/',
            method: "POST",
            data: {
                text: original_text,
                rot: $scope.user_rot,
                action: action
            }
        }).then(loadSuccess, loadError);
    };

    $scope.find_key = function (){
        if($scope.is_guess){
            return;
        }
        $scope.is_guess = true;
        original_text = $('#original_text').val();

        $http({
            url: 'find_key_view/',
            method: "POST",
            data: {
                text: original_text
            }
        }).then(findKeySuccess, findKeyError);
    };

    var findKeySuccess = function (response) {
        if(response.data.guess_rot != 0){
            $scope.guess_rot = response.data.guess_rot;
        }
        $scope.is_guess = false;
    };

    var findKeyError = function (response) {
        $scope.is_guess = false;
    };

});


function createChart(chart_data){
    $('#myChart').remove();
    $('#myChartContainer').append('<canvas id="myChart" height="70px"></canvas>');
    ctx = document.getElementById("myChart").getContext("2d");
    myBarChart = new Chart(ctx).Bar(chart_data);
}