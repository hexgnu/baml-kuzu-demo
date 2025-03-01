class Medicine {
    generic_name string
    brand_names string[]
    // This entire item will only stream when complete
    @@stream.done
}

class ConditionAndMedicine {
    condition string
    medicine Medicine[]
    side_effects string[]
}

function ExtractFromImage(img: image) -> ConditionAndMedicine[] {
  client OpenRouterGPT4oMini
  prompt #"
    Extract the condition, medicine names and side effects from the provided table with these columns:
    - Reason for medicine
    - Medicine names: Generic name & (Brand name)
    - Side effects

    {{ ctx.output_format }}

    DO NOT INCLUDE QUOTES IN YOUR JSON RESPONSE.

    {{ _.role("user") }}
    {{ img }}
  "#
}

test TestOne {
  functions [ExtractFromImage]
  args {
    img {
      file "../../files/images/medicine_1.png"
    }
  }
}
