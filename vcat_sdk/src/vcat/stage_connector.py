class StageConnector(object):

    def __init__(self, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None
        self._is_persisted = False

    def name(self):
        return self.current_stage.name()

    def function_name(self):
        return self.current_stage.function_name()

    def args(self):
        return self.current_stage.args

    def kwargs(self):
        return self.current_stage.kwargs

    def persist(self):
        self._is_persisted = True

    def _fold_tree(self, fold_action):
        parent_results = [connector._fold_tree(fold_action) for connector in self._previous_connectors]
        return fold_action(parent_results, self)

    def _reset_state(self):
        def reset_action(parent_results, this_connector):
            this_connector._has_run = False
            this_connector._result = None

        self._fold_tree(reset_action)

    def add_tree_names(self, stages_dict, filler_builder, **filler_kwargs):
        def add_tree_names_action(parent_ids, this_connector):
            filler = filler_builder(*this_connector.args(), **this_connector.kwargs())
            args, kwargs = filler.fill(**filler_kwargs)
            this_stage = {"function_name": this_connector.function_name(
                ), "args": args, "kwargs": kwargs, "parents": parent_ids}
            stages_dict[this_connector.name()] = this_stage
            return this_connector.name()

        return self._fold_tree(add_tree_names_action)

    def stage(self, next_stage):
        return StageConnector(next_stage, [self])

    def run(self, filler_builder, **filler_kwargs):
        def run_action(previous_results, this_connector):
            if this_connector._has_run:
                return this_connector._result
            else:
                this_connector._result = this_connector.current_stage.run(
                    previous_results, filler_builder, **filler_kwargs)
                this_connector._has_run = True
                return this_connector._result

        return self._fold_tree(run_action)