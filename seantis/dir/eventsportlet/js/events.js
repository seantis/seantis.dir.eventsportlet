var load_events = function($) {

    var from_iso = function(date) {
        // see http://stackoverflow.com/a/11021320
        var D= new Date('2011-06-02T09:34:29+02:00');
        if(!D || +D!== 1307000069000){
            var day, tz,
            rx=/^(\d{4}\-\d\d\-\d\d([tT ][\d:\.]*)?)([zZ]|([+\-])(\d\d):(\d\d))?$/,
            p= rx.exec(date) || [];
            if(p[1]){
                day= p[1].split(/\D/);
                for(var i= 0, L= day.length; i<L; i++){
                    day[i]= parseInt(day[i], 10) || 0;
                }
                day[1]-= 1;
                day= new Date(Date.UTC.apply(Date, day));
                if(!day.getDate()) return NaN;
                if(p[5]){
                    tz= (parseInt(p[5], 10)*60);
                    if(p[6]) tz+= parseInt(p[6], 10);
                    if(p[4]== '+') tz*= -1;
                    if(tz) day.setUTCMinutes(day.getUTCMinutes()+ tz);
                }
                return day;
            }
            return NaN;
        } else {
            return new Date(date);
        }
    };

    var get_event_tag = function(val, count, max) {
        var className = "portletItem" +
                        ((count % 2) ? " odd" : " even") +
                        ((count == max) ? " lastItem" : "");
        var startDate = from_iso(val.start);
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

    var find_and_fill_events = function() {
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

(function($){
    $(document).ready(function() {
        load_events($);
    });
})(jQuery);
