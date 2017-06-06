/*removes leading and trailing whitespace. IE compliant*/
function trimWhiteSpace(s){
    return s.replace( /^[ \t]+|[ \t]+$/,'');
}

function extendFilters() {
    jQuery.extend(jQuery.expr[':'], {
        organization:function(elem, index, m) {
            m[0] = m[0].replace(/:organization\(|\)$/g, '');
            if('oid'+m[0]+'_'=='oidALL_')return true;
            var $elem = $(elem);
            var oid = $elem.attr('oid');
            if (oid === undefined) return false;
            var val1 = 'oid' + oid + '_';
            var val2 = 'oid' + m[0] + '_';
            return val1 == val2;
        },
        text_search:function(elem, index, m) {
            m[0] = m[0].replace(/:text_search\(|\)$/g, '');
            if('ts'+m[0]+'_'=='ts_')return true;
            var $elem = $(elem);
            var ts = 'ts' + m[0];
            ts = ts.toLowerCase();
            var rv = false;
            var $tds = $('td',$elem);
            $tds.each(function(i){
            	var val1 = 'ts' + $(this).html().toLowerCase();
            	if(val1.startsWith(ts)){
            	 	rv = true;
            	 	return false;
            	}
            });
            return rv;
        }
    });
}

function disableEnter(e){
  var key = window.event ? e.keyCode : e.which;
  if(key==13)return false;
  else return true;
}

String.prototype.startsWith = function(str){
	return (this.indexOf(str) === 0);
}
function detectIE(){
  if (navigator.appName == 'Microsoft Internet Explorer')
    {
      //document.getElementById("IEwarning").classList.add("alert alert-danger")
      result = "You are using Microsoft Internet Explorer <br> this application is optimized for Firefox and Chrome <br>"
      return document.getElementById("detectIEresult").innerHTML = result;
    }
  }
