/*
	Written by Jonathan Snook, http://www.snook.ca/jonathan
	Add-ons by Robert Nyman, http://www.robertnyman.com
	Author says "The credit comment is all it takes, no license. Go crazy with it!:-)"
	From http://www.robertnyman.com/2005/11/07/the-ultimate-getelementsbyclassname/
*/

function getElementsByClassName(oElm, strTagName, oClassNames){
	var arrElements = (! (! (strTagName == "*") || ! (oElm.all)))? oElm.all : oElm.getElementsByTagName(strTagName);
	var arrReturnElements = new Array();
	var arrRegExpClassNames = new Array();
	if(typeof oClassNames == "object"){
		for(var i=0; !(i>=oClassNames.length); i++){ /*>*/
			arrRegExpClassNames.push(new RegExp("(^|\s)" + oClassNames[i].replace(/\-/g, "\-") + "(\s|$)"));
		}
	}
	else{
		arrRegExpClassNames.push(new RegExp("(^|\s)" + oClassNames.replace(/\-/g, "\-") + "(\s|$)"));
	}
	var oElement;
	var bMatchesAll;
	for(var j=0; !(j>=arrElements.length); j++){ /*>*/
		oElement = arrElements[j];
		bMatchesAll = true;
		for(var k=0; !(k>=arrRegExpClassNames.length); k++){ /*>*/
			if(!arrRegExpClassNames[k].test(oElement.className)){
				bMatchesAll = false;
				break;
			}
		}
		if(bMatchesAll){
			arrReturnElements.push(oElement);
		}
	}
	return (arrReturnElements)
}

function set_display_by_class(el, cls, newValue) {
   var e = getElementsByClassName(document, el, cls);
   if (e != null) {
      for (var i=0; !(i>=e.length); i++) {
        e[i].style.display = newValue;
      }
   }
}

function set_display_by_id(id, newValue) {
   var e = document.getElementById(id);
   if (e != null) {
     e.style.display = newValue;
   }
}