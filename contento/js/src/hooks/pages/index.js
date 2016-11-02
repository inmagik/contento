import React from 'react'
import { render } from 'react-dom'
import PagesContainer from './components/PagesContainer'

export default (element) => {
  const pages = JSON.parse(element.value || '[]')

  const container = document.createElement('div')
  element.parentNode.insertBefore(container, element)
  // element.style.visibility = 'hidden'

  const save = (data) => element.value = JSON.stringify(data)

  render(<PagesContainer pages={pages} save={save} />, container)
}
