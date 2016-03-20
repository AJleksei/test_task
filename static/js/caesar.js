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
    $scope.guess_rot = null;
    $scope.user_rot = null;
    $scope.is_guess = false;



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

    var loadSuccess = function (response) {
        $scope.text = response.data.text;
    };

    var loadError = function (response) {
        /*
        $.each(response.data.errors, function(key, value){
            alert(value);
        });
        */
    };

    function rebuildChart (){
        original_text = $('#original_text').val();
        chart_data = getDataChart(original_text);
        createChart(chart_data);
    }

    $scope.find_key = function (){
        if($scope.is_guess){
            return;
        }
        $scope.is_guess = true;
        original_text = $('#original_text').val();
        if(original_text.length == 0){
            $scope.is_guess = false;
            deleteChart();
            $scope.guess_rot = null;
            return;
        }

        trim_text = original_text.substring(0, 5000);

        $http({
            url: 'find_key_view/',
            method: "POST",
            data: {
                text: trim_text
            }
        }).then(findKeySuccess, findKeyError);

        rebuildChart();
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

function deleteChart(){
    if($("canvas").is($("#myChart"))){
        $("#myChart").remove();
    }
}

function createChart(chart_data){
    deleteChart();
    $('#myChartContainer').append('<canvas id="myChart" height="70px"></canvas>');
    ctx = document.getElementById("myChart").getContext("2d");
    myBarChart = new Chart(ctx).Bar(chart_data);
}

function getDataChart(text){
    letters_count = {};
    for (var i = 0; i < text.length; i++) {
        val = 1;
        letter = text[i].toLowerCase();
        if (letter in letters_count){
            val = letters_count[letter] + 1;

        }
        letters_count[letter] = val;
    }

    data_data = [];
    labels_data = [];
    $.each(letters_count, function(key, val){
        //alert('key = ' + key + '\nvalue = ' + val);
        data_data.push(val);
        labels_data.push(key);
    });
    chart_data = {
        labels: labels_data,
        datasets: [
            {
                label: "Letters rating",
                fillColor: "rgba(0,102,204, 0.5)",// Цвет колонки
                strokeColor: "rgba(0,51,153, 0.8)",// Цвет рамки, вокруг колонки
                highlightFill: "rgba(0,51,153, 0.75)",
                highlightStroke: "rgba(0,51,153, 1)",
                data: data_data
            }
        ]
    };
    return chart_data;
}