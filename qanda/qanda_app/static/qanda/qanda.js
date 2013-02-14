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