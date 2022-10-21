<script>
  moment.locale("de")

  fields = document.getElementsByClassName("date-time")

  for (let field of fields) {

    value = field.textContent
    value_new = moment(value).format("LLL")
    field.textContent = value_new
  }
</script>
