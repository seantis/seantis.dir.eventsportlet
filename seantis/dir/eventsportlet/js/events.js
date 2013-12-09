var load_events = function($) {

    var get_event_tag = function(val, count, max){
        var className = "portletItem" +
                        ((count % 2) ? " odd" : " even") +
                        ((count == max) ? " lastItem" : "");
        var startDate = new Date(val.start);
        var dateText = startDate.getDate() + '.' +
                      (startDate.getMonth()+1) + '.' +
                       startDate.getFullYear();

        return '<dd class="' + className + '">' +
               '<p class="eventDate">' + dateText + '</p>' +
               '<p class="eventTitle">' +
                    '<a href="' + val.origin + '">' + val.title + '</a>' +
               '</p>' +
               '</dd>';
    };

    var find_and_fill_events = function () {
        $(document).find('dd[data-event-config-url][data-event-config-max]').each(function(){
            var url = $(this).attr('data-event-config-url');
            var max = $(this).attr('data-event-config-max');
            var portlet = $(this);
            $.getJSON(url, function(data) {
                var events = [];
                var count = 0;
                $.each(data, function(key, val) {
                    if (count++<max) {
                        events.push(get_event_tag(val, count, max));
                    }
                });
                $(portlet).replaceWith(events.join(''));
            });
        });
    };

    find_and_fill_events();
};

load_libraries(['jQuery'], function($) {
    $(document).ready(function() {
        load_events($);
    });
});