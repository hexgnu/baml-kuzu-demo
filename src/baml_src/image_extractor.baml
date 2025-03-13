// Extract drug information and its known side effects from a table in an image
class Drug {
    generic_name string
    brand_names string[] @description("Strip the ® character at the end of the brand names")
}

class ConditionAndDrug {
    condition string
    drug Drug[]
    side_effects string[]
}

function ExtractFromImage(img: image) -> ConditionAndDrug[] {
  client OpenRouterGPT4oMini
  prompt #"
    You are an expert at extracting healthcare and pharmaceutical information.

    Extract the condition, drug names and side effects from these columns:
    - Reason for drug
    - Drug names: Generic name & (Brand name)
    - Side effects

    {{ ctx.output_format }}

    {{ _.role("user") }}
    {{ img }}
  "#
}

test TestOne {
  functions [ExtractFromImage]
  args {
    img {
      file "../../data/img/drugs_1.png"
    }
  }
}

test TestTwo {
  functions [ExtractFromImage]
  args {
    img {
      file "../../data/img/drugs_2.png"
    }
  }
}
