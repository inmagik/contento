import React, {PropTypes} from 'react';
import Pages from './Pages'
import { Sortable } from 'react-sortable'

const Page = ({ page, hierarchyKey, updatePages, ...sortableProps }) => (
  <div className="" {...sortableProps}>
    <div className="alert alert-info">
      <div className="pull-left">
        {page.label}<br />
        <span className="text-muted">{page.url}</span>
      </div>
      <div className="pull-right">
        <a
          className="btn btn-sm btn-primary"
          href={page.editUrl}
        >
          Edit
        </a>

        {' '}

        <a className="btn btn-sm btn-primary"
          href={page.viewUrl}>
          View
        </a>
        {' '}
        <a
          className="btn btn-sm btn-primary"
          href={page.addChildUrl}>
          Add child
        </a>
        {' '}
        <a
          className="btn btn-sm btn-danger"
          href={page.dropUrl}>
          Drop
        </a>

      </div>
      <div className="clearfix"></div>
    </div>
    <div style={{marginLeft: '2em'}}>
      <Pages
        hierarchyKey={hierarchyKey}
        updatePages={updatePages}
        pages={page.children}
      />
    </div>
</div>
)

const SortablePage = Sortable(Page)
export default SortablePage
