//
//  SecondaryViewController.swift
//  safetracker
//
//  Created by Rohit Dsouza on 20/12/18.
//  Copyright © 2018 Rohit Dsouza. All rights reserved.
//

import UIKit

class SecondaryViewController: UIViewController {
    
    @IBOutlet weak var dispCords: UILabel!
    
    var data:Cords?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        dispCords.text = "\(String(describing: data?.lat)), \(String(describing: data?.long))"
        self.navigationItem.leftItemsSupplementBackButton = true
        
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        let backItem = UIBarButtonItem()
        backItem.title = "Back"
        navigationItem.backBarButtonItem = backItem
        
        if(segue.identifier == "showCrimeDist"){
            
            let destinationViewController = segue.destination as? VisualViewController
            
            present(destinationViewController!, animated: true, completion: nil)
        }
    }
    
    @IBAction func showCrimeChart(_ sender: Any) {
        
        self.performSegue(withIdentifier: "showCrimeDist", sender: self)
        
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
