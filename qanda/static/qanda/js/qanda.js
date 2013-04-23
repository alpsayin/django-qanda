function clearAllText(thefield)
{
	if (thefield.defaultValue==thefield.value)
		thefield.value = ""
} 

function checkUncheck(element1, element2) 
{
	var c1 = document.getElementById(element1);
	var c2 = document.getElementById(element2);
	if (c1.type == 'checkbox' & c2.type == 'checkbox')
	{
		if (c1.checked & c2.checked)
		{
			c2.checked = false;
		}
	}
}

function toggleElementVisibility(element, message_display, message_hide, speed)
{
	$(element).toggle(speed, function(){
		if ( $(element).is(":visible") )
		{
			$(message_display).toggle()
			$(message_hide).toggle()
		}
		else
		{
			$(message_display).toggle()
			$(message_hide).toggle()
		}
	});
}

function confirmRedirect(message, redirect_url_true, redirect_url_false)
{
	var retVal = confirm(message);
	if(retVal==true)
	{
		window.location.href = redirect_url_true;
	}
	else
	{
		window.location.href = redirect_url_false;
	}
}

var popup_displayed = 0

$(document).ready(function()
{
	$(".container").click(function()
	{
		if( popup_displayed == 1)
		{
			$("#popup").toggle(function(){ popup_displayed = 0 })
		}
	});
	
	$(".popup-display").click(function()
	{
		if($("#popup").css("display") == "none")
		{
			$("#popup").toggle(function(){ popup_displayed = 1 })
		}
	});
});