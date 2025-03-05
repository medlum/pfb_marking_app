import streamlit as st

st.title(' :orange[Why ☕ ?]')
#st.divider()
text = """

Hey there! If you’ve found my work helpful, consider buying me a coffee - it’s a small but meaningful way to show your support.

- It helps me keep going - Developing and maintaining this takes time, and your support keeps me motivated.

- It keeps things free - I love sharing my work with everyone, and a coffee helps cover costs like hosting and development tools.

- It encourages new features - Your support lets me dedicate more time to improving and expanding what I offer.

- It’s a simple way to say thanks - If you’ve benefited from my work, this is an easy way to show appreciation.

Every coffee means a lot, thanks for being awesome!


"""
st.markdown(f'<span style="text-align: justify; font-size:20px; color:#242320;">{text}</span>', unsafe_allow_html=True)

#st.divider()

pay_instruction = "(Buy Andy a coffee with the QR code!)"
st.markdown(f'<span style="text-align: justify; font-size:15px; color:#242320;">{pay_instruction}</span>', unsafe_allow_html=True)
st.image('paynowME.jpeg', width=250)