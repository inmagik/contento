import React, {PropTypes} from 'react';
import Pages from './Pages'
import { SortableHandle, SortableElement } from 'react-sortable-hoc'

const DragHandle = SortableHandle(() => (
  <div style={{
    cursor: 'move',
    borderBottomLeftRadius: '4px',
    borderTopLeftRadius: '4px',
    border: '1px solid transparent',
    margin: '-16px',
    lineHeight: '80px',
    color: '#31708f',
    textAlign: 'center',
    height: '80px',
    background: '#bce8f1',
    width: '12px'
  }}>
   <span>{' '}</span>
   {/* <i className="glyphicon glyphicon-option-vertical" /> */}
  </div>
))

const Page = ({ page, hierarchyKey, togglePage, updatePages }) => (
  <div className="">
    <div className="alert alert-info">
      <div className="pull-left">
        <DragHandle />
      </div>
      <div>
        <div className="pull-left">
          <div className="pull-left" style={{ paddingRight: '5px' }}>
            {!!page.children.length && (
              <i
                onClick={() => togglePage(hierarchyKey, page)}
                style={{ cursor: 'pointer' }}
                className={`glyphicon glyphicon-chevron-${page.toggled ? 'down' : 'right'}`}
              />
            )}
            {!page.children.length && (
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
    </div>
    {page.toggled && page.children.length && (
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

export default SortableElement(Page)
