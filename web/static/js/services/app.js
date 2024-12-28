(function () {
    'use strict';

    angular.module('myApp').service('SharedService', ['$cookies', '$http', function ($cookies, $http) {
        const url_user_info = "api/user/info"


        this.getToken = function () {
            return $cookies.get('token') || undefined;
        };
        this.setToken = function (newCookie) {
            $cookies.put('token', newCookie);
        };

    }]);
}());