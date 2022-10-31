<script>
  moment.locale("de")

  fields = document.getElementsByClassName("date-time")

  for (let field of fields) {

    value = field.textContent

    if (field.classList.contains("date-no-year")) {
      value_new = moment(value).format("DD. MMM")
    } else {
      value_new = moment(value).format("LLL")
    }
    field.textContent = value_new
  }
</script>
