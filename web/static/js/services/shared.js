(function () {
    'use strict';

    angular.module('myApp').service('SharedService', ['$window', '$rootScope', function ($window, $rootScope) {
        console.log('SharedService loaded')
        this.getToken = function () {
            return $window.localStorage.getItem('access_token')
        };
        this.setToken = function (token) {
            $window.localStorage.setItem('access_token', token)
            $rootScope.$broadcast('tokenUpdate');
        };
        this.isAuthenticated = function () {
            return !!this.getToken();
        };
    }]);
}());