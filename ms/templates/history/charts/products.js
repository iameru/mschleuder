function pickColor(exclude=null) {
  let color_palette  = [ "#824638", "#CE9587" , "#A86758" , "#6B2D1F" , "#491509" , "#825F38" , "#CEAD87" , "#A88258" , "#6B471F" , "#492B09" , "#254552" , "#577582" , "#3A5B6A" , "#163644" , "#08222E" , "#285E3E" , "#619476" , "#3F7857" , "#164D2C" , "#073419"]
  if (exclude) {
    color_palette = color_palette.filter(color => color != exclude)
  }
  return color_palette[Math.floor(Math.random() * color_palette.length)]
}
const productButtons = document.getElementById('products-buttons')
const productName = document.getElementById('product-name')
let currentProductId
const productDetails = document.getElementById('product-details')
const allProductsButton = document.getElementById('all-products-button')
const clearChartButton = document.getElementById('clear-chart-button')
const startDatePicker = document.getElementById('start-date-picker')
const endDatePicker = document.getElementById('end-date-picker')
const productChartArea = document.getElementById('product-chart-area')

const ctx = document.getElementById('product-chart');

function createChart(ctx) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [{
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      parsing: {
        xAxisKey: 'distribution_date',
        yAxisKey: 'value',
      },
      layout: {
        padding: 23,

      },
    }
  })
}

// fetch all product names
async function fetchProducts() {
  let result = []
  await fetch('{{ url_for("history.api_products")}}')
    .then(response => response.json())
    .then(data => {
      result = data
    })
    .catch(error => console.log("error:", error))
  return result
}

async function fetchProduct(id) {
  let result = []
  await fetch(`{{ url_for("history.api_product") }}?product_id=${id}&start_date=${startDatePicker.value}&end_date=${endDatePicker.value}`)
    .then(response => response.json())
    .then(data => {
      result = data
    })
    .catch(error => console.log("error:", error))
  return result
}

function deleteCharts() {
  productChartArea.childNodes.forEach(child => {
    child.remove()
  })
  productChartArea.innerHTML = ''
}

async function select(id) {
  deleteCharts()
  // we selected a product and want to display it's data now
  document.getElementById(`product-${currentProductId}`)?.classList.remove('is-active')
  document.getElementById(`product-${id}`).classList.add('is-active')

  const product = await fetchProduct(id)
  productName.innerHTML = product.name
  currentProductId = product.id


  // get the keys aka unit_names and their values aka datasets
  Object.keys(product.data).forEach(key => {

    lolColor = pickColor()
    canvas = document.createElement('canvas')
    canvas.id = `${key}-canvas-${product.id}`
    // # set raw color as style with transparency 0.1
    canvas.style.backgroundColor = lolColor + '12'
    unit_name = product.data[key].unit_name
    unit_total = product.data[key].total
    data = product.data[key].data

    chart = createChart(canvas)

    chart.options.plugins.subtitle = {
      display: true,
      text: `Gesamt: ${Math.round(unit_total * 100) / 100} ${unit_name}`,
    }

    if (data.length <= 3) {
      chart.config.type = 'bar'

    } else {
      chart.config.type = 'line'
    }


    chart.data.datasets = [{
      data: data,
      borderColor: lolColor,
      backgroundColor: lolColor,
      label: unit_name,
    }]

    productChartArea.appendChild(canvas)
  })

  if (productChartArea.childNodes.length == 0) {
    productChartArea.innerHTML = `Keine Daten zu ${product.name} vorhanden`
  }
}

async function updateChart() {
  await select(currentProductId)
}

async function main() {

  endDatePicker.value = new Date().toISOString().split('T')[0]
  const products = await fetchProducts()

  products.sort((a, b) => a.name.localeCompare(b.name))
  // build some sweet *** button element with it
  products.map(product => {
    
    node = allProductsButton.cloneNode()
    node.id = `product-${product.id}`
    node.innerHTML = product.name
    node.classList.remove('is-hidden')
    node.onclick = () => select(product.id)
    productButtons.appendChild(node)

    })
}

main()
