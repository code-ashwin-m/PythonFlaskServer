(function () {
    'use strict';

    angular.module('myApp').service('TokenService', ['$cookies', function ($cookies) {
        this.getToken = function () {
            return $cookies.get('token') || undefined;
        };
        this.setToken = function (newCookie) {
            $cookies.put('token', newCookie);
        };
    }]);
}());