
import streamlit as st
from dataclasses import dataclass, field
import uuid

state = st.session_state

from styles import apply_page_theme


st.set_page_config(page_title="To-do list", page_icon="icons/list-check.png")

apply_page_theme()


st.logo("imgs/logo.png")


st.markdown("""
<style>
    .stTextInput input {
        color: #ffffff;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stForm {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)


@dataclass
class Todo:
    text: str
    is_done = False
    uid: uuid.UUID = field(default_factory=uuid.uuid4)


if "todos" not in state:
    state.todos = [
        Todo(text="Do homework"),
        Todo(text="Clean room"),
        Todo(text="Study for test"),
    ]


def remove_todo(i):
    state.todos.pop(i)


def add_todo():
    state.todos.append(Todo(text=state.new_item_text))
    state.new_item_text = ""


def check_todo(i, new_value):
    state.todos[i].is_done = new_value


def delete_all_checked():
    state.todos = [task for task in state.todos if not task.is_done]


with st.container(horizontal_alignment="center"):
    st.title(
        ":orange[:material/checklist:] To-do list",
        width="content",
        anchor=False,
    )

with st.form(key="new_item_form", border=False):
    with st.container(
        horizontal=True,
        vertical_alignment="bottom",
    ):
        st.text_input(
            "New item",
            label_visibility="collapsed",
            placeholder="Add to-do item",
            key="new_item_text",
        )

        st.form_submit_button(
            "Add",
            icon=":material/add:",
            on_click=add_todo,
        )

if state.todos:
    with st.container(gap=None, border=True):
        for i, task in enumerate(state.todos):
            with st.container(horizontal=True, vertical_alignment="center"):
                st.checkbox(
                    task.text,
                    value=task.is_done,
                    width="stretch",
                    on_change=check_todo,
                    args=[i, not task.is_done],
                    key=f"todo-chk-{task.uid}",
                )
                st.button(
                    ":material/delete:",
                    type="tertiary",
                    on_click=remove_todo,
                    args=[i],
                    key=f"delete_{i}",
                )

    with st.container(horizontal=True, horizontal_alignment="center"):
        st.button(
            ":small[Delete all checked]",
            icon=":material/delete_forever:",
            type="tertiary",
            on_click=delete_all_checked,
        )

else:
    st.info("No to-do items. Go fly a kite! :material/family_link:")


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)