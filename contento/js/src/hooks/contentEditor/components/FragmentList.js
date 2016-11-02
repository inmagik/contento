import React from 'react';
import { SortableContainer } from 'react-sortable-hoc'
import Fragment from './Fragment'

const FragmentList = ({ name, fragments, fragmentsSchemas, updateFragmentData, updateFragment, removeFragment }) => (
  <div>
    {fragments.map((fragment, index) =>
      <Fragment
        key={`region-${name}-fragment-${index}`}
        index={index}
        collection={name}
        fragment={fragment}
        fragmentTitle={fragmentsSchemas[fragment.type].title}
        schema={fragmentsSchemas[fragment.type]}
        updateFragment={(frag) => updateFragment(index, frag)}
        updateFragmentData={(data) => updateFragmentData(index, data)}
        removeFragment={() => removeFragment(index)}
      />
    )}
  </div>
)

export default SortableContainer(FragmentList)
