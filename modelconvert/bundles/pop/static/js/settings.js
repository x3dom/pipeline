 var HeaderSettings = function()
{
	this.showFPS = false;
	this.showErrorBound = false;
	this.showTitle = false;
	this.showTriangles = true;
}

var PopLimitedValue = function()
{
	this.min = 0;
	this.max = 10;
	this.value = 5;
	this.getPercentage = function()
	{
		return (this.value/this.max)*100;
	};

	this.getCurrentValueString = function()
	{
		return (this.value.toString()); // + " / " + this.max.toString());
	}
}

PopGeoData = function()
{
	this.renderPoints = false;
	this.renderedTriangles = new PopLimitedValue();
	this.renderedSubMeshes = new PopLimitedValue();
	this.errorBound = 1;
	this.minPrecBits = 16;
	this.maxPrecBits = 0;
	this.getPrecBitsString = function()
	{
		return (this.minPrecBits+ " - " + this.maxPrecBits);
	};
	this.precisionBitsString  = this.getPrecBitsString();
};

popGeoData = new PopGeoData();
headerSettings = new HeaderSettings();

usePopLevelTexture = false;