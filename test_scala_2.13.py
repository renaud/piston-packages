#!/usr/bin/env python3
"""
Test script for Scala 2.13.16 Piston package.
Run this after setting up the GitHub repository and configuring Piston.
"""

import requests
import json

PISTON_URL = "http://localhost:2000/api/v2/execute"

def test_scala_code(name, code):
    """Execute Scala code and print results."""
    payload = {
        "language": "scala",
        "version": "2.13.16",
        "files": [{"name": "main.scala", "content": code}],
        "compile_timeout": 10000,
        "run_timeout": 3000,
    }
    
    try:
        response = requests.post(PISTON_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n{'='*60}")
        print(f"Test: {name}")
        print(f"{'='*60}")
        
        # Show compilation output
        if "compile" in result:
            if result["compile"]["code"] == 0:
                print("✓ Compilation: SUCCESS")
            else:
                print("✗ Compilation: FAILED")
                if result["compile"]["stderr"]:
                    print(f"Compilation Error:\n{result['compile']['stderr']}")
                return False
        
        # Show execution output
        if "run" in result:
            if result["run"]["code"] == 0:
                print("✓ Execution: SUCCESS")
                print(f"\nOutput:\n{result['run']['stdout']}")
            else:
                print("✗ Execution: FAILED")
                if result["run"]["stderr"]:
                    print(f"Error:\n{result['run']['stderr']}")
                return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        return False

# Test cases
test_cases = [
    ("Traditional main method", """
object Hello {
  def main(args: Array[String]): Unit = {
    println("Hello from Scala 2.13 with main method!")
    val numbers = List(1, 2, 3, 4, 5)
    val doubled = numbers.map(_ * 2)
    println(s"Doubled: ${doubled.mkString(", ")}")
  }
}
"""),
    
    ("App trait", """
object HelloApp extends App {
  println("Hello from Scala 2.13 with App trait!")
  val words = List("Scala", "is", "awesome")
  println(words.mkString(" "))
}
"""),
    
    ("Case classes and pattern matching", """
object PatternTest {
  def main(args: Array[String]): Unit = {
    sealed trait Shape
    case class Circle(radius: Double) extends Shape
    case class Rectangle(width: Double, height: Double) extends Shape
    
    def area(shape: Shape): Double = shape match {
      case Circle(r) => math.Pi * r * r
      case Rectangle(w, h) => w * h
    }
    
    val circle = Circle(5.0)
    val rect = Rectangle(4.0, 6.0)
    
    println(s"Circle area: ${area(circle)}")
    println(s"Rectangle area: ${area(rect)}")
  }
}
"""),
    
    ("Higher-order functions", """
object FunctionalTest extends App {
  val numbers = (1 to 10).toList
  
  val evens = numbers.filter(_ % 2 == 0)
  println(s"Even numbers: ${evens.mkString(", ")}")
  
  val sum = numbers.reduce(_ + _)
  println(s"Sum: $sum")
  
  val factorial = (1 to 5).foldLeft(1)(_ * _)
  println(s"5! = $factorial")
}
"""),
]

def main():
    print("Scala 2.13.16 Piston Package Test Suite")
    print("="*60)
    
    # Check if Scala 2.13.16 is installed
    try:
        response = requests.get("http://localhost:2000/api/v2/runtimes")
        runtimes = response.json()
        scala_2_13 = any(r["language"] == "scala" and r["version"] == "2.13.16" for r in runtimes)
        
        if not scala_2_13:
            print("\n✗ ERROR: Scala 2.13.16 is not installed!")
            print("\nInstall it with:")
            print('curl -X POST -H "Content-Type: application/json" \\')
            print('  -d \'{"language":"scala","version":"2.13.16"}\' \\')
            print('  http://localhost:2000/api/v2/packages')
            return
        
        print("✓ Scala 2.13.16 is installed\n")
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ ERROR: Cannot connect to Piston API: {e}")
        print("\nMake sure Piston is running:")
        print("docker ps | grep piston_api")
        return
    
    # Run all tests
    results = []
    for name, code in test_cases:
        success = test_scala_code(name, code)
        results.append((name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Scala 2.13.16 is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    main()

