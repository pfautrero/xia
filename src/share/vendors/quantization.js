class Quantization {
  constructor() {

  }
  /*
   *  Define Image
   */
  setImage(image) {
    var canvas_source = document.createElement('canvas')
    canvas_source.setAttribute('width', image.width);
    canvas_source.setAttribute('height', image.height);
    var context_source = canvas_source.getContext('2d')
    context_source.drawImage(image,0,0, image.width, image.height)
    var imageDataSource = context_source.getImageData(0, 0, image.width, image.height);
    this.imageData = imageDataSource.data
    this.image = image

  }

  /*
   * Split pixels in 3 families : RED, BLUE and GREEN
   */
  firstFilter() {
    var redColors = []
    var blueColors = []
    var greenColors = []
    for(var varx = 0; varx < this.image.width; varx +=5) {
      for(var vary = 0; vary < this.image.height; vary +=5) {
        var position1 = 4 * (vary * this.image.width + varx)
        var red = this.imageData[position1 + 0]
        var green = this.imageData[position1 + 1]
        var blue = this.imageData[position1 + 2]
        var alpha = this.imageData[position1 + 3]
        if (alpha > 200) {
          if ((red >= green) && (red >= blue)) redColors.push({
            'red' : red,
            'green' : green,
            'blue' : blue
          })
          if ((green >= red) && (green >= blue)) greenColors.push({
            'red' : red,
            'green' : green,
            'blue' : blue
          })
          if ((blue >= red) && (blue >= green)) blueColors.push({
            'red' : red,
            'green' : green,
            'blue' : blue
          })
        }
      }
    }

    var max = Math.max(redColors.length, greenColors.length, blueColors.length)
    if (redColors.length == max) return redColors
    if (greenColors.length == max) return greenColors
    if (blueColors.length == max) return blueColors
  }

  /*
   * Split once more time colors
   */
  secondFilter(colorArray, color1, color2) {
    var color1Array = []
    var color2Array = []
    for(var i = 0; i < colorArray.length; i +=1) {
      if (colorArray[i].color1 >= colorArray[i].color2) {
        color1Array.push({
          'red' : colorArray[i].red,
          'green' : colorArray[i].green,
          'blue' : colorArray[i].blue
        })
      }
      else {
        color2Array.push({
          'red' : colorArray[i].red,
          'green' : colorArray[i].green,
          'blue' : colorArray[i].blue
        })
      }
    }
    var max = Math.max(color1Array.length, color2Array.length)
    if (color1Array.length == max) return color1Array
    if (color2Array.length == max) return color2Array

  }

  /*
   * calculate average color from array colors
   */
  calculateAverage(colorArray) {
    var finalColor = {
      'red' : 0,
      'green' : 0,
      'blue' : 0
    }
    for(var i = 0; i < colorArray.length; i +=1) {
      finalColor.red += colorArray[i].red
      finalColor.green += colorArray[i].green
      finalColor.blue += colorArray[i].blue
    }
    finalColor.red = Math.floor(finalColor.red / colorArray.length)
    finalColor.green = Math.floor(finalColor.green / colorArray.length)
    finalColor.blue = Math.floor(finalColor.blue / colorArray.length)
    return finalColor
  }

  /*
   * get dominant color using MEDIAN CUT algorithm
   */
  getDominantColor() {

    var firstArray = this.firstFilter()
    var secondArray = []

    var red = firstArray[0].red
    var green = firstArray[0].green
    var blue = firstArray[0].blue

    if ((red >= green) && (red >= blue)) {
      secondArray = this.secondFilter(firstArray, 'green', 'blue')
    }
    else if ((green >= red) && (green >= blue)) {
      secondArray = this.secondFilter(firstArray, 'red', 'blue')
    }
    else if ((blue >= red) && (blue >= green)) {
      secondArray = this.secondFilter(firstArray, 'green', 'red')
    }

    return this.calculateAverage(secondArray)
  }
}
