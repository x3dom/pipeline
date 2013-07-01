



/*****************************************
 * JQuery plugin
 *
 * makes it possible to just select the text of an element but
 * no child elements content
 *
 * http://viralpatel.net/blogs/2011/02/jquery-get-text-element-without-child-element.html
 **************************************/
jQuery.fn.justtext = function () {
    return $(this).clone()
        .children()
        .remove()
        .end()
        .text();
};

/*
 * it provides functions that are described in the book "JavaScript the Good Parts"
 * This functions and techniques are very helpful to write good and clean code!!!
 *
 * Module that hides all its variables in closures (private variables)
 */
var jsGoodParts = (function () {
    "use strict";
    return {
        init : function () {
            Function.prototype.method = function (name, func) {
                if (!this.prototype[name]) {
                    this.prototype[name] = func;
                    return this;
                }
            };
            Number.method("integer", function () {
                return Math[this < 0 ? 'ceil' : 'floor'](this);
            });
            String.method("trim", function () {
                return this.replace(/^\s+|\s+$/g, '');
            });
        },

        /*
         * checks if the argument is an Object
         * Objects can be real Objects or Arrays
         */
        isObject : function (obj) {
            if (obj && typeof obj === 'object') {
                return true;
            }
            return false;
        },
        /*
         * checks if the argument is an Object
         * This function excludes Arrays!
         */
        isRealObject : function (obj) {
            if (obj && typeof obj === 'object' && !this.isArray(obj)) {
                return true;
            }
            return false;
        },
        /*
         * checks if the argument is an Array
         * This function excludes Objects!
         */
        isArray : function (obj) {
            if (obj && typeof obj === 'object' && typeof obj.length === 'number' && !(obj.propertyIsEnumerable('length'))) {
                return true;
            }
            return false;
        }
    };
}());
