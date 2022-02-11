class LabelColourSelector:
    def __init__(self, project):
        self._project = project

    def get_colour(self, label):
        if (label in ('jira-type:task', 'jira-type:story', 'Task', 'Story', 'story')): return '7bc043'
        elif (label == 'Bug'): return 'ee4035'
        # elif (label in self._project.get_components()): return 'fdf498'
        # elif (label.replace('component:', '') in self._project.get_components()): return 'fdf498'
        else: return 'ededed'