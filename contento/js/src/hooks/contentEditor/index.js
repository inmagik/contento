import React from 'react'
import { render } from 'react-dom'
import ContentEditor from './components/ContentEditor'

export default (element) => {
  const givenRegios = JSON.parse(element.value || '{}');
  const allEmptyRegions = JSON.parse(element.getAttribute('data-contenteditor-regions') || '[]')
    .reduce((all, name) => ({ ...all, [name]: [] }), {})
  const regions = { ...allEmptyRegions, ...givenRegios }

  const fragmentsSchemas = JSON.parse(element.getAttribute('data-contenteditor-fragments-schemas') || '{}')

  const container = document.createElement('div')
  element.parentNode.insertBefore(container, element)

  // if (process.env.NODE_ENV === 'production') {
  //   element.style.height = 0;
  //   element.style.visibility = 'hidden'
  // }
  const save = regions => element.value = JSON.stringify(regions)

  render(
    <ContentEditor
      fragmentsSchemas={fragmentsSchemas}
      regions={regions}
      save={save}
    />,
    container
  )
}
