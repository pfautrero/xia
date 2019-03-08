//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//   You should have received a copy of the GNU General Public License
//   along with this program.  If not, see <http://www.gnu.org/licenses/>
//
//
// @author : pascal.fautrero@gmail.com


// Script used to load youtube resource after main page
// otherwise, Chrome fails to start the page

$(".videoWrapper16_9").each(function(){
    var source = $(this).data("iframe");
    var iframe = document.createElement("iframe");
    iframe.src = source;
    $(this).append(iframe);
    $(this).data("iframe", "");
});

$(".videoWrapper4_3").each(function(){
    var source = $(this).data("iframe");
    var iframe = document.createElement("iframe");
    iframe.src = source;
    $(this).append(iframe);
    $(this).data("iframe", "");
});
$(".flickr_oembed").each(function(){
    var source = $(this).data("oembed");
    var that = $(this);
    $.ajax({
        url: "http://www.flickr.com/services/oembed/?format=json&callback=?&jsoncallback=xia&url=" + source,
        dataType: 'jsonp',
        jsonpCallback: 'xia',
        success: function (data) {
            var url = data.url;
            var newimg = document.createElement("img");
            newimg.src = url;
            that.append(newimg);
        }
    });
});
