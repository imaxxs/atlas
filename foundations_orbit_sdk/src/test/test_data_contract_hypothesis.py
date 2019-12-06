from hypothesis import given, assume, example, settings
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, columns, data_frames
from pandas import DataFrame
from foundations_orbit.data_contract import DataContract

from foundations_spec import Spec


@st.composite
def dataframes(draw, *strategies: st.SearchStrategy) -> st.SearchStrategy:
    names = draw(st.lists(st.integers(), unique=True, min_size=1))
    cols = [column(name, elements=draw(st.sampled_from(strategies))) for name in names]
    return draw(data_frames(cols))


class TestDataContractHypothesis(Spec):
    
    @given(dataframes(st.booleans()))
    @example(DataFrame({"a": [False] * 100 + [True]}))  # 99:1 bug
    @settings(deadline=None)
    def test_validation_with_categorical_data_does_not_blow_up(self, df: DataFrame):
        assume(not df.empty)
        with self.assert_does_not_raise():
            DataContract("my_contract", df).validate(df)