import type { SidebarsConfig } from '@docusaurus/plugin-content-docs'

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Concepts',
      items: ['concepts/lie-groups', 'concepts/action-angles', 'concepts/connection']
    },
    {
      type: 'category',
      label: 'Results',
      items: ['results/staeckel-potential', 'results/variable-delta', 'results/measuring-results']
    }
  ]
}

export default sidebars
