angular.module("myApp", [])
.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
})
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
})
.controller('CaesarController', function ($scope, $http){
        $scope.text = null;
        $scope.letters_count = null;
        $scope.guess_rot = null;
        $scope.user_rot = null;

         $scope.load = function ($event){
            original_text = $('#original_text').val();
            $scope.user_rot = $('#rot').val();
            action = $event.currentTarget.name;

            $http({
                url: 'test/',
                method: "POST",
                data: {
                    text: original_text,
                    rot: $scope.user_rot,
                    action: action
                },
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            }).then(function successCallback(response) {
                $scope.text = response.data.text;
                $scope.guess_rot = response.data.guess_rot;

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

                document.getElementById("myChart").remove();
                $('#myChartContainer').append('<canvas id="myChart" height="70px"></canvas>');
                ctx = document.getElementById("myChart").getContext("2d");
                $scope.myBarChart = new Chart(ctx).Bar(chart_data);
            }, function errorCallback(response) {
                 alert('Ошибка!');
            });
        };
    }
);

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }
