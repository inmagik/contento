import React from 'react'
import { SortableContainer } from 'react-sortable-hoc'
import Page from './Page'

const collectionIdentifier = (hierarchyKey) => {
  if (hierarchyKey.length === 0) {
    return '/'
  }
  return hierarchyKey[hierarchyKey.length - 1]
}

const PageList = ({ pages, hierarchyKey, updatePages, togglePage }) => (
  <div>
    {pages.map((page, index) =>
      <Page
        key={page.viewUrl}
        index={index}
        collection={collectionIdentifier(hierarchyKey)}
        page={page}
        hierarchyKey={hierarchyKey}
        updatePages={updatePages}
        togglePage={togglePage}
      />
    )}
  </div>
)

export default SortableContainer(PageList)
