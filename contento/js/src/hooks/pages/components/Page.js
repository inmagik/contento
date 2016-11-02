import React, {PropTypes} from 'react';
import Pages from './Pages'
import { Sortable } from 'react-sortable'

const Page = ({ page, hierarchyKey, togglePage, updatePages, ...sortableProps }) => (
  <div className="" {...sortableProps}>
    <div className="alert alert-info">
      <div className="pull-left">
        <div className="pull-left" style={{ paddingRight: '5px' }}>
          {(page.children.length > 0) && (
            <i
              onClick={() => togglePage(hierarchyKey, page)}
              style={{ cursor: 'pointer' }}
              className={`glyphicon glyphicon-chevron-${page.toggled ? 'down' : 'right'}`}
            />
          )}
          {(page.children.length === 0) && (
            <i className="glyphicon glyphicon glyphicon-file" />
          )}
        </div>
        <div className="pull-left">
          {page.label}<br />
          <span className="text-muted">{page.url}</span>
        </div>
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
    {page.toggled && (
      <div style={{marginLeft: '2em'}}>
        <Pages
          hierarchyKey={[...hierarchyKey, page.viewUrl]}
          togglePage={togglePage}
          updatePages={updatePages}
          pages={page.children.map(page => page)}
        />
      </div>
    )}
</div>
)

const SortablePage = Sortable(Page)
export default SortablePage
