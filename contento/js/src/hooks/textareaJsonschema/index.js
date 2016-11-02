import React from 'react'
import { render } from 'react-dom'
import Form from 'react-jsonschema-form'

export default (element) => {
  const value = JSON.parse(element.value || '{}');
  const schema = JSON.parse(element.getAttribute('data-textarea-jsonschema') || '{}')

  const container = document.createElement('div')
  element.parentNode.insertBefore(container, element)
  // element.style.visibility = 'hidden'

  const handleChange = ({ formData }) => {
    element.value = JSON.stringify(formData);
  }

  const TextareaForm = (
    <Form schema={schema} formData={value} onChange={handleChange}>
      <div/>
    </Form>
  )

  render(TextareaForm, container)
}
